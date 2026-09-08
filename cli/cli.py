import os
import pathlib
import re
import shutil
import sys
import termios
from pathlib import Path

import requests
import ultraclick as click
from ultraclick import ctx

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class ServiceType(click.ParamType):
    """
    Custom Click type for dynamic service name completion using the 'docker services' command.
    """
    name = "service"

    def shell_complete(self, param, incomplete):
        """
        Provide tab-completion for services by invoking the 'docker services' command.
        """
        with click.output.silence():

            # Step 1: Forward to the MainCommand to initialize it
            main_command_ctx = ctx.find_root()
            main_command_ctx.forward(main_command_ctx.command)

            docker_command_ctx = ctx.parent
            main_command_ctx.invoke(docker_command_ctx.command)

            # Step 4: Get the 'services' command from the DockerCommand group
            services_command = docker_command_ctx.command.get_command(docker_command_ctx, "services")

            if not services_command:
                raise ValueError("Services command could not be found in DockerCommand.")

            # Step 5: Invoke the 'services' command to fetch services
            services = docker_command_ctx.invoke(services_command)

        # Provide completion for environment variables
        return [click.shell_completion.CompletionItem(k) for k in services if k.startswith(incomplete)]

# -------------------------------
# Nested Group Classes
# -------------------------------

class GroupDeep:
    """
    Deep nested group with its own commands.
    """
    def __init__(self, other):
        self.other = other

    @click.command()
    @click.argument("name")
    def greet(self, name):
        """Example subcommand: prints a greeting."""
        env = ctx.meta.get("env", "unknown")
        return f"Greeting {name} in environment '{env}' with other={self.other}."

    @click.command()
    def farewell(self):
        """Example subcommand: says goodbye."""
        env = ctx.meta.get("env", "unknown")
        return f"Goodbye from GroupDeep. Environment: {env}"

class GitCommand:
    """
    Git helper commands
    """

    def __init__(self):
        pass

    @click.command()
    @click.argument("commit_message")
    def push(self, commit_message="Iterate"):
        """Add all changed files, commit them, and push to the remote repository."""
        # 1) Stage all changes
        click.run("git add -A", headline="Staging all changes")

        # 2) Commit changes with the provided commit message
        click.run(f'git commit -m "{commit_message}"', headline="Committing changes")

        # 3) Push changes to the remote repository
        click.run("git push", headline="Pushing to remote repository")

        # 4) Show status
        click.run("git status", headline="Showing status")

class GroupTwo:
    """
    Subcommands for group2.
    """
    deep = GroupDeep

    def __init__(self, docker_flag):
        self.docker_flag = docker_flag

    @click.command()
    def ping(self):
        """Ping subcommand."""
        return f"Pong from GroupTwo. Docker flag: {self.docker_flag}"

    @click.command()
    def version(self):
        """Show version info from GroupTwo."""
        return f"GroupTwo version 1.0.0"

class DockerCommand:
    """
    Manage Docker and Docker Compose tasks.
    """

    def __init__(self):
        """Initialize the Docker command group."""
        # Retrieve values global context
        self.env = ctx.meta['env']
        self.docker_dir = ctx.meta['docker_dir']
        self.docker_compose_file = ctx.meta['docker_compose_file']
        self.frontend_dir = ctx.meta['frontend_dir']

        # Build the base Docker Compose command
        self._dc_cmd = self._build_dc_cmd()

        os.environ["COMPOSE_MENU"] = "0"
        #os.environ["LINES"] = click.output.run_command('tput lines').stdout.strip()
        #os.environ["COLUMNS"] = click.output.run_command('tput cols').stdout.strip()

    @click.command(context_settings={"ignore_unknown_options": True})
    @click.argument("args", nargs=-1)
    def compose(self, args):
        """Run Docker Compose commands."""
        # Should not return the function return value as it leads to duplicate output
        self._run_dc_cmd(' '.join(args), headline="Running Docker Compose command")

    @click.command()
    @click.argument("services", nargs=-1, type=ServiceType())
    def follow(self, services):
        services = " ".join(ctx.invoke(self.services, services=services))
        return self._run_dc_cmd(f'logs -f {services}', headline=f'Following {services}')

    @click.command()
    @click.argument("service_name", required=True)
    @click.argument("source_path", required=True)
    @click.argument("destination", required=True)
    @click.option("--force", is_flag=True, help="Force overwriting the destination directory.")
    def rsync_app(self, service_name, source_path, destination, force):
        """Sync app files from a service's container."""
        self._remove_destination(destination, force)
        os.makedirs(destination, exist_ok=True)
        container_id = self._get_container_id(service_name)
        if container_id:
            self._copy_from_container(container_id, source_path, destination)
            return f"Successfully synced '{source_path}' from service '{service_name}' to '{destination}'."
        else:
            return f"Failed to sync '{source_path}' from service '{service_name}'. Container not found."

    @click.command()
    @click.argument("services", nargs=-1)
    @click.option("-a", "--all", is_flag=True, help="Include all services, even those without a specified Dockerfile.")
    def base(self, services, all):
        """
        Retrieve the base image repository and version of the specified Docker SERVICES.
        If no services are provided, retrieve all services.
        """

        # Retrieve Dockerfile paths and base images for all services
        services_info = ctx.invoke(self.services, dockerfiles=True, base_images=True)

        # Filter the services if specific ones are provided
        if services:
            services_info = {service: services_info[service] for service in services if service in services_info}

        if not all:
            # Exclude services with no Dockerfile or base images
            services_info = {
                service: details
                for service, details in services_info.items()
                if details and details[0] is not None  # Check for Dockerfile path presence
            }

        click.output.headline("Resolving base image versions for services")

        resolved_versions = {}
        for service, details in services_info.items():
            #dockerfile_path = details[0]  # First value is the Dockerfile path
            base_images = details[1:]  # Remaining values are base images

            if not base_images:
                resolved_versions[service] = "No base images specified"
                continue

            latest_versions = []
            for base_image in base_images:
                try:
                    # Extract repository and tag from the base image
                    repo, tag = (base_image.split(":") + ["latest"])[:2]  # Handle images without a tag
                    if "/" not in repo:
                        repo = f"library/{repo}"  # Prefix with "library/" for official images

                    # Fetch the digest for the specified tag
                    latest_url = f"https://hub.docker.com/v2/repositories/{repo}/tags/{tag}/"
                    click.output.info(f"Fetching digest for tag '{tag}' from: {latest_url}")

                    latest_response = requests.get(latest_url)
                    latest_response.raise_for_status()
                    latest_digest = latest_response.json()["images"][0]["digest"]

                    # Fetch all tags and find the matching version
                    tags_url = f"https://hub.docker.com/v2/repositories/{repo}/tags/?page_size=100"
                    click.output.info(f"Fetching all tags from: {tags_url}")
                    tags_response = requests.get(tags_url)
                    tags_response.raise_for_status()
                    tags_data = tags_response.json()["results"]

                    matching_tags = [
                        tag_data["name"]
                        for tag_data in tags_data
                        if tag_data["images"][0]["digest"] == latest_digest and tag_data["name"] != "latest"
                    ]

                    latest_versions.append(matching_tags[0] if matching_tags else f"Tag: {tag}, Digest: {latest_digest}")
                except Exception as e:
                    latest_versions.append(f"Error resolving version: {str(e)}")

            # Combine all resolved versions for the service
            resolved_versions[service] = latest_versions

        # Return resolved versions
        return resolved_versions

    @click.command()
    @click.argument("service", type=ServiceType())
    @click.argument("source_path")
    @click.argument("destination_path", type=click.Path(exists=False, file_okay=False, dir_okay=True, resolve_path=True))
    @click.option("--force", is_flag=True, help="Force overwriting the destination directory.")
    def base_copy(self, service, source_path, destination_path, force):
        """
        Copy files from the base image of the specified SERVICE.
        """
        # Get base images for all services
        services_info = ctx.invoke(self.services, base_images=True)
        if service not in services_info:
            click.output.error(f"Service '{service}' not found.")
            return

        # Get the base image for the service
        base_images = services_info[service]
        if not base_images:
            click.output.error(f"Service '{service}' does not specify a base image.")
            return

        # Use the first base image (primary one in multi-stage builds)
        base_image = base_images[0]

        # Prepare the destination path
        dest_path = Path(destination_path).resolve()
        if dest_path.exists():
            if not force:
                click.output.error(f"Destination '{destination_path}' already exists. Use --force to overwrite.")
                return
            click.output.info(f"Removing existing destination: {destination_path}")
            shutil.rmtree(dest_path)
        os.makedirs(dest_path, exist_ok=True)

        click.output.headline(f"Copying from base image '{base_image}'")

        # Step 1: Create a temporary container from the base image
        try:
            create_cmd = f"docker create {base_image}"
            container_id = click.output.run_command(create_cmd, suppress=True).stdout.strip()
            if not container_id:
                click.output.error(f"Failed to create container from base image '{base_image}'.")
                return

            # Step 2: Copy files from the container
            copy_cmd = f"docker cp {container_id}:{source_path} {destination_path}"
            click.output.run_command_and_print_output(copy_cmd, headline=f"Copying files from '{base_image}'")

            click.output.success(f"Successfully copied '{source_path}' from base image '{base_image}' to '{destination_path}'.")

        except Exception as e:
            click.output.error(f"Error during base copy: {str(e)}")
        finally:
            # Step 3: Remove the temporary container
            if 'container_id' in locals():
                click.output.run_command(f"docker rm {container_id}", suppress=True)

    @click.command()
    @click.argument("original_path", type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
    @click.argument("modified_path", type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
    @click.argument("output_path", type=click.Path(file_okay=False, dir_okay=True, writable=True, resolve_path=True))
    @click.option("--replace-threshold", type=float, default=0.5, help="Threshold (in % of lines) above which a file is replaced instead of patched.")
    @click.option("--force", is_flag=True, help="Force overwrite of the output directory.")
    @click.option(
        "--exclude-dirs",
        type=str,
        help="Comma-separated list of directories to exclude from processing.",
        show_default=True,
    )
    def generate_patches(self, original_path, modified_path, output_path, replace_threshold, force=False, exclude_dirs="tmp,log,packs"):
        """
        Compare directory trees and generate patches or replacements for files that differ.
        Excludes certain directories specified in --exclude-dirs and skips symlinks.
        """
        original_path = Path(original_path).resolve()
        modified_path = Path(modified_path).resolve()
        output_path = Path(output_path).resolve()

        exclude_dirs = set(exclude_dirs.split(","))

        if output_path.exists() and not force:
            click.output.error(f"Output path '{output_path}' already exists. Use --force to overwrite.")
            return

        if output_path.exists() and force:
            shutil.rmtree(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        click.output.headline(f"Generating patches and replacements in '{output_path}'")

        for root, dirs, files in os.walk(modified_path, followlinks=False):
            root_path = Path(root)

            # Exclude directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file_name in files:
                modified_file = root_path / file_name

                # Skip symlinks
                if modified_file.is_symlink():
                    #click.output.info(f"Skipping symlink: {modified_file}")
                    continue

                relative_path = modified_file.relative_to(modified_path)
                original_file = original_path / relative_path
                output_file_dir = output_path / relative_path.parent

                if not original_file.exists():
                    # File does not exist in the original -> replace completely
                    click.output.info(f"Adding new file: {relative_path}")
                    output_file_dir.mkdir(parents=True, exist_ok=True)  # Create directory only when needed
                    shutil.copy(modified_file, output_file_dir)
                    continue

                # Check if the files are identical
                #if filecmp.cmp(original_file, modified_file, shallow=False):
                #    # Files are identical -> skip
                #    continue

                # Compare files using `diff`
                try:

                    diff_cmd = f"diff -u -d -N -w -B -i {original_file} {modified_file}"
                    result = click.output.run_command(diff_cmd, silent=True, error_handling=False)

                    if result.returncode == 0:
                        # Files are identical (additional safety check)
                        continue

                    #click.output.info(f'Looking at {original_file}')
                    #click.output.info(f'{diff_cmd}')

                    diff_output = result.stdout
                    insertions, deletions, modifications = 0, 0, 0

                    prev_deleted = False  # Tracks whether the previous line was a deletion

                    for line in diff_output.splitlines():
                        if line.startswith("+") and not line.startswith("+++"):
                            if prev_deleted:
                                # Count this as a modification, not a separate change
                                modifications += 1
                                deletions -= 1
                                # Reset deletion tracker
                                prev_deleted = False
                                #click.output.echo ('Modification')
                            else:
                                #click.output.echo ('Insertion')
                                insertions += 1
                        elif line.startswith("-") and not line.startswith("---"):
                            #click.output.echo ('Deletion')
                            prev_deleted = True
                            deletions += 1
                    # Adjust total changes: Count modifications only once, subtracting them from insertions/deletions
                    total_changes = insertions + deletions + modifications
                    total_lines = sum(1 for _ in open(original_file))
                    # Compute change ratio
                    change_ratio = total_changes / max(total_lines, 1)

                    #click.output.info(f'Change ratio: {change_ratio} = {total_changes} / {total_lines}')

                    if change_ratio > replace_threshold:
                        # Replace the file completely
                        click.output.info(f"\nReplacing large change file: '{relative_path}' (Change ratio: {change_ratio:.2%})")
                        output_file_dir.mkdir(parents=True, exist_ok=True)
                        click.output.info(output_file_dir)
                        click.output.info(relative_path)
                        shutil.copy(modified_file, output_file_dir)
                    else:
                        # Save the diff as a patch
                        patch_file = output_file_dir / f"{file_name}.patch"
                        click.output.info(f"\nGenerating patch for file: '{relative_path}' (Change ratio: {change_ratio:.2%})")
                        click.output.info(patch_file)
                        output_file_dir.mkdir(parents=True, exist_ok=True)
                        with open(patch_file, "w") as patch:
                            #pattern = r'^(---|\+\+\+)([^\t]+)\t[\S]+$'
                            #pattern = r'^(---|\+\+\+)\s+(\S+).*$'
                            # Replace with just the header marker and file path
                            #diff_output = re.sub(pattern, r'\1 \2', diff_output, flags=re.MULTILINE)
                            patch.write(diff_output)

                except Exception as e:
                    click.output.error(f"Error comparing files '{original_file}' and '{modified_file}': {str(e)}")

        click.output.success(f"Patches and replacements saved in '{output_path}'.")

    @click.command()
    @click.argument("services", type=ServiceType(), nargs=-1)
    @click.option("--no-pull", is_flag=True, help="Do not pull the latest base image before building.")
    @click.option("--no-cache", is_flag=True, help="Build the image without using cache.")
    def build(self, services, no_pull, no_cache):
        """
        Build the Docker image(s) for the specified SERVICES using 'docker compose build'.
        If no services are specified, build all services.
        """
        # Get Dockerfile paths and base images for all services
        services_info = ctx.invoke(self.services, dockerfiles=True, base_images=True)

        # Default to building all services if none are specified
        if not services:
            services = list(services_info.keys())

        # Filter services based on user input
        services_info = {svc: services_info[svc] for svc in services if svc in services_info}

        for service, details in services_info.items():
            dockerfile_path = details[0]  # Dockerfile path
            base_images = details[1:]  # Base images

            # Step 1: Pull the latest base images (unless --no-pull is specified)
            if not no_pull:
                for base_image in base_images:
                    try:
                        pull_cmd = f"docker pull {base_image}"
                        click.output.run_command_and_print_output(pull_cmd, headline=f"Pulling '{service}' service base image")
                    except Exception as e:
                        click.output.error(f"Error pulling base image {base_image}: {str(e)}")
                        continue

            # Step 2: Use docker compose to build the service
            try:
                build_cmd = f"{self._dc_cmd} build {service}"
                if no_cache:
                    build_cmd += " --no-cache"
                if not no_pull:
                    build_cmd += " --pull"

                build_cmd += "  --progress=plain"

                click.output.run_command_and_print_output(build_cmd, headline=f"Building '{service}' service")
            except Exception as e:
                click.output.error(f"Error building image for service {service}: {str(e)}")

    @click.command()
    @click.argument("service_name", required=True, type=ServiceType())
    @click.argument("mount_point", type=click.Path(), required=False)
    @click.option("-r", "--rebind", is_flag=True, help="Unmount the existing mount first before bind mounting.")
    def bind(self, service_name, mount_point, rebind):
        """
        Generate and execute a bindfs command for the filesystem root of a running service.
        """
        # Default mount point to DOCKER_DIR/SERVICE_NAME/root if not provided
        if not mount_point:
            mount_point = os.path.join(self.docker_dir, service_name, "root")

        # Convert mount_point to an absolute path for internal operations
        mount_point_abs = os.path.abspath(mount_point)

        # Ensure the mount point directory exists
        os.makedirs(mount_point_abs, exist_ok=True)

        # Check if the mount point is already in use
        is_mounted = False
        with open("/proc/mounts", "r") as mounts_file:
            for line in mounts_file:
                if mount_point_abs in line:
                    is_mounted = True
                    break

        # Unmount if --rebind is specified and the mount point is in use
        if rebind and is_mounted:
            click.output.info(f"Unmounting existing mount at '{mount_point}'")
            cmd = f"sudo umount {mount_point_abs}"
            click.output.run_command_and_print_output(cmd, headline=f"Unmounting '{mount_point}'")
        elif is_mounted:
            click.output.error(f"The mount point '{mount_point}' is already in use. Use '--rebind' to unmount it first.")
            return

        # Invoke the pids command to get the PID for the specified service
        try:
            pids = ctx.invoke(self.pids, services=[service_name])
        except Exception as e:
            click.output.error(f"Failed to retrieve PID for service '{service_name}': {e}")
            return

        # Extract the PID for the service
        pid = pids.get(service_name)
        if not pid:
            click.output.error(f"Could not retrieve PID for service '{service_name}'. Ensure the service is running.")
            return

        # Construct the bindfs command with user mapping
        current_user = os.getlogin()
        fs_root = f"/proc/{pid}/root"
        bind_command = (
            f"sudo bindfs --map=root/{current_user} --mirror-only={current_user} "
            f"{fs_root} {mount_point_abs}"
        )

        # Execute the bindfs command
        click.output.run_command_and_print_output(bind_command, headline=f"Binding '{fs_root}' to '{mount_point}'")

        click.output.success(f"Successfully bound '{fs_root}' to '{mount_point}'")

    @click.command(no_args_is_help=False)
    @click.argument("services", nargs=-1, required=False)
    @click.option("--dockerfiles", "-f", is_flag=True, help="Include Dockerfile paths for each service.")
    @click.option("--base-images", "-b", is_flag=True, help="Include base images for each service.")
    @click.option("--pids", "-p", is_flag=True, help="Include running PIDs for each service.")
    @click.option("--all", "-a", is_flag=True, help="Include all services, even if they have no values.")
    def services(self, services=None, dockerfiles=False, base_images=False, pids=False, all=False):
        """
        List services with optional details.
        """

        # Step 1: Fetch all available services
        cmd = f"{self._dc_cmd} config --format=json"
        compose_data = click.output.run_command_and_parse_json(cmd, headline="Listing services")

        if not isinstance(compose_data, dict):
            raise ValueError("Failed to parse Docker Compose configuration.")

        available_services = compose_data.get("services", {}).keys()

        # Step 2: Filter by specific services if provided
        if services:
            available_services = [s for s in available_services if s in services]

        # Step 3: Return a plain list if no flags are provided
        if not (dockerfiles or base_images or pids):
            return list(available_services)

        # Step 4: Initialize services_info with plain lists
        services_info = {service: [] for service in available_services}

        # Step 5: Extract details
        if dockerfiles or base_images:
            self._fetch_service_dockerfiles(services_info, compose_data)

        if base_images:
            self._fetch_service_base_images(services_info, keep_dockerfiles=dockerfiles)

        if pids:
            self._fetch_service_pids(services_info)

        # Step 6: Filter services based on `--all`
        if not all:
            services_info = {service: details for service, details in services_info.items() if details}

        # Step 7: Return detailed service info
        return services_info

    @click.command()
    @click.argument("services", nargs=-1, type=ServiceType())
    @click.option("-a", "--all", is_flag=True, help="Include all services, even those not running.")
    def pids(self, services, all):
        """
        Retrieve the PIDs of the specified Docker services.
        """
        # Delegate to the services command with the `--pids` flag
        services_with_pids = ctx.invoke(self.services, services=services, pids=True)

        # Include all services if `--all` is specified
        if all:
            all_services = ctx.invoke(self.services)
            for service in all_services:
                if service not in services_with_pids:
                    services_with_pids[service] = {"pid": ""}

        # Display or return PIDs
        return {service: details[0] for service, details in services_with_pids.items()}

    # Helper Functions
    def _fetch_service_pids(self, services_info):
        """
        Append PIDs to the services_info lists.
        """
        for service in services_info.keys():
            get_id_cmd = f"docker ps --filter 'name={service}' --format '{{{{.ID}}}}'"
            result = click.output.run_command(get_id_cmd, suppress=True, error_handling=False)
            container_ids = result.stdout.strip().splitlines()

            if not container_ids:
                continue

            container_id = container_ids[0]
            get_pid_cmd = f"docker inspect --format '{{{{.State.Pid}}}}' {container_id}"
            result = click.output.run_command(get_pid_cmd, suppress=True, error_handling=False)
            pid = result.stdout.strip()

            if pid != "0":
                services_info[service].append(pid)

    def _fetch_service_base_images(self, services_info, keep_dockerfiles=True):
        """
        Append base images to the services_info lists, optionally keeping Dockerfile paths.

        Args:
            services_info (dict): The dictionary containing service details.
            keep_dockerfiles (bool): Whether to retain Dockerfile paths in the lists.
        """
        for service, details in services_info.items():
            dockerfile_path = details[0] if details else None  # Assume Dockerfile path is the first item
            if not dockerfile_path:
                continue

            try:
                with open(dockerfile_path, "r") as df:
                    base_images = [line.split()[1] for line in df if line.strip().startswith("FROM")]
                    if not keep_dockerfiles:
                        details.clear()  # Remove the Dockerfile if overwriting
                    details.extend(base_images)
            except FileNotFoundError:
                if not keep_dockerfiles:
                    details.clear()

    def _fetch_service_dockerfiles(self, services_info, compose_data):
        """
        Append Dockerfile paths to the services_info lists.
        """
        services = compose_data.get("services", {})
        for service, details in services.items():
            build_details = details.get("build", {})
            dockerfile = build_details.get("dockerfile", "Dockerfile")
            context = build_details.get("context", ".")
            dockerfile_path = str(Path(context) / dockerfile)
            services_info[service].append(dockerfile_path)

    # Internal Helper Methods
    def _build_dc_cmd(self):
        return (
            f"docker compose -f {self.docker_compose_file} "
            f"--env-file={os.path.join(self.docker_dir, f'{self.env}.env')}"
        )

    def _run_dc_cmd(self, cmd, **kwargs):
        return click.output.run_command(f"{self._dc_cmd} {cmd}",**kwargs)

    def _get_container_id(self, service_name):
        cmd = f"{self._dc_cmd} ps -q {service_name}"
        result = click.output.run_command(cmd, headline=f"Getting container ID for {service_name}", suppress=True, error_handling=False)
        if not result.stdout.strip():
            click.output.error(f"No running container found for service: {service_name}")
            return None
        return result.stdout.strip()

    def _remove_destination(self, destination, force):
        dest_path = Path(destination).resolve()
        if dest_path.exists():
            if not force:
                click.output.error(f"Destination '{destination}' already exists. Use --force to overwrite.")
                sys.exit(1)
            click.output.info(f"Removing existing destination: {destination}")
            shutil.rmtree(dest_path)

    def _copy_from_container(self, container_id, source_path, destination):
        if not source_path.endswith('/'):
            source_path += '/'
        cmd = f"docker cp {container_id}:{source_path} {destination}"
        click.output.run_command(cmd, headline="Copying files from container")

# -------------------------------
# UpdatesCommand Class
# -------------------------------

class UpdatesCommand:
    """
    Show and install package updates for pip, npm, and docker.
    """

    def __init__(self):
        """Initialize the update command group."""
        # Initialize environment variables
        self.env = ctx.meta.get('env', 'unknown')
        self.frontend_dir = ctx.meta.get('frontend_dir', pathlib.Path('./frontend'))

    @click.command()
    @click.argument("target", type=click.Choice(["all", "pip", "npm"]), default="all")
    def show(self, target):
        """Show updates for the selected target."""
        if target == "all":
            self._show_pip_updates()
            self._show_npm_updates()
        elif target == "pip":
            self._show_pip_updates()
        elif target == "npm":
            self._show_npm_updates()

    @click.command()
    @click.argument("target", type=click.Choice(["all", "pip", "npm"]), default="all")
    def install(self, target):
        """Install updates for the selected target."""
        if target == "all":
            self._install_pip_updates()
            self._install_npm_updates()
        elif target == "pip":
            self._install_pip_updates()
        elif target == "npm":
            self._install_npm_updates()

    def _show_pip_updates(self):
        click.output.run_command("pip list --outdated", headline="Showing 'pip' updates")

    def _install_pip_updates(self):
        click.output.headline("Installing 'pip' updates...")
        # Run the command and get the parsed JSON output
        outdated_packages = click.output.run_command(
            "pip list --outdated --format=json", parse_json=True, suppress=True
        )

        if not isinstance(outdated_packages, list) or not outdated_packages:
            click.output.success("All packages are up-to-date.")
            return

        try:
            # Extract package names
            package_names = " ".join(pkg["name"] for pkg in outdated_packages)
            if not package_names:
                click.output.success("All packages are up-to-date.")
                return

            # Install updates
            click.output.run_command(f"pip install --upgrade {package_names}")
            click.output.success("Packages updated successfully.")
        except KeyError:
            click.output.error("Unexpected format in pip list output.")
            click.output.failure("Could not retrieve outdated pip packages.")

    def _show_npm_updates(self):
        if not self.frontend_dir.is_dir():
            click.output.error("No 'frontend' directory found.")
            return
        cmd = f"cd {self.frontend_dir} && npm outdated"
        res = click.output.run_command(cmd, headline="Showing 'npm' updates", error_handling=False)
        if res.returncode == 0:
            click.output.success("'npm' is up-to-date.")


    def _install_npm_updates(self):
        click.output.headline("Installing 'npm' updates...")

        # Ensure the frontend directory exists
        if not self.frontend_dir.is_dir():
            click.output.error("No 'frontend' directory found.")
            return

        # Navigate to the frontend directory and check for outdated packages
        outdated_command = f"cd {self.frontend_dir} && npm outdated --json"
        outdated_packages = click.output.run_command(outdated_command, parse_json=True, suppress=True, error_handling=False)

        if not outdated_packages:
            click.output.success("All npm packages are up-to-date.")
            return

        try:
            # Prepare a summary of packages to be updated
            packages_to_update = [
                f"{pkg} (current: {details['current']}, latest: {details['latest']})"
                for pkg, details in outdated_packages.items()
            ]
            click.output.info("The following packages will be updated:")
            for package in packages_to_update:
                click.output.info(f"  - {package}")

            # Run the npm update command
            update_command = f"cd {self.frontend_dir} && npm update"
            click.output.run_command(update_command, suppress=False)

            # Summarize updated packages
            click.output.success("Packages updated successfully.")
            click.output.info("Updated packages:")
            for package in packages_to_update:
                click.output.success(f"  - {package}")
        except Exception as e:
            click.output.error(f"Failed to install npm updates: {e}")
            click.output.failure("Could not update npm packages.")


# -------------------------------
# MainGroup Class
# -------------------------------

class MainGroup:
    """
    Main CLI group with top-level commands and subgroups.
    """
    git = GitCommand
    group2 = GroupTwo
    updates = UpdatesCommand
    docker = DockerCommand

    @click.option("--env", default="dev", envvar='ENV', help="Environment to use (e.g., dev, prod).")
    @click.option("--frontend-dir", default="./frontend", type=pathlib.Path, help="Frontend directory.")
    @click.option("--docker-dir", default="./docker", type=pathlib.Path, help="Docker directory.")
    @click.option("--docker-compose-file", default="./docker/docker-compose.yml", type=pathlib.Path, help="Docker compose file.")
    def __init__(self, **kwargs):
        """MAIN CLI"""

        # Assign all keyword arguments dynamically to both self and ctx.meta
        for key, value in kwargs.items():
            setattr(self, key, value)
            ctx.meta[key] = value

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')

        #TODO: Put in ultraclick
        if sys.stdin.isatty():
            fd = sys.stdin.fileno()
            attr = termios.tcgetattr(fd)
            # clear the ECHOCTL bit to not print control characters like ^C
            attr[3] &= ~termios.ECHOCTL
            termios.tcsetattr(fd, termios.TCSANOW, attr)

        # Warn if not in a virtual environment
        #if sys.prefix == sys.base_prefix and "VIRTUAL_ENV" not in os.environ:
        #    click.output.warning("Virtual environment is not active. It is recommended to activate one before using this CLI.")

    @click.command()
    @click.argument("target", type=click.Choice(['front', 'static', 'all']), default="all")
    def build(self, target):
        """Build production frontend assets and collect Django static files."""
        if target in ['all', 'front']:
            click.run(["npm", "--prefix", self.frontend_dir, "run", "build"], headline="Building frontend assets")

        if target in ['all', 'static']:
            return ctx.forward(self.django_admin, args=("collectstatic", "--noinput"))

    @click.command()
    @click.argument("target", type=click.Choice(['front', 'back', 'worker', 'all']), default="back")
    @click.argument("host", default="0.0.0.0:8000")
    def run(self, target, host):
        """Run development servers"""
        #cmd = "DEBUG=true python manage.py runserver 0.0.0.0:8000"
        if target in ['all', 'back']:
            click.run([sys.executable, "./cli/manage.py", "dev", host], headline="Running backend dev server (Django)")
        if target in ['all', 'front']:
            click.run(["npm", "--prefix", self.frontend_dir, "run", "dev"], headline="Running frontend dev server (NPM)")

    dev = click.alias(run)

    @click.command()
    @click.argument("rev", required=False)
    def pull(self, rev):
        """Bring the checkout to REV, or to the branch's newest commit, and install its dependencies"""
        if rev:
            click.run("git fetch", headline="Fetching")
            click.run(["git", "checkout", rev], headline=f"Checking out {rev}")
        else:
            click.run("git pull", headline="Pulling")
        click.run([sys.executable, "-m", "pip", "install", "--group", "backend/pyproject.toml:main"], headline="Installing backend dependencies")
        click.run(["npm", "--prefix", self.frontend_dir, "install"], headline="Installing frontend dependencies")

    @click.command()
    def deploy(self):
        """Build the image from the last build and start it"""
        ctx.invoke(self.docker.build, services=('django',), no_pull=False, no_cache=False)
        ctx.invoke(self.docker.compose, args=('up', '-d'))

    @click.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
    @click.argument("args", nargs=-1)
    def django_admin(self, args, **kwargs):
        """Django management command"""
        click.output.headline(f'Running django-admin')
        #It's not actually using manage.py, this is just a placeholder because
        #the very first argument is ignored by django-admin
        args = ['manage.py', *args]
        import djultra.management.commands.fastmanage_patch
        from django.core.management import execute_from_command_line
        execute_from_command_line(args)

    @click.command()
    def status(self):
        """Display the current status."""


        #TODO: Identify lines and columns when needed

        click.output.headline(f'Terminal')
        click.output.info(f'Got "{click.output.lines}" lines and "{click.output.columns}" columns')

        click.output.headline(f'Environment')
        click.output.info(f"Name: {self.env}\nFrontend dir: {self.frontend_dir}\nDocker dir: {self.docker_dir}")


# -------------------------------
# CLI Entry Point
# -------------------------------

if __name__ == "__main__":
    # Create the CLI using MainGroup
    cli = click.group_from_class(MainGroup)
    cli(prog_name="dm")
