import os
import shutil
from pathlib import Path
from invoke import Collection, task

import setup
from utils.command_executor import CommandExecutor
from utils.logger import INFO, print_task_documentation


@task(pre=[setup.setup_context])
@print_task_documentation
def detect_profile(ctx):
    """
    Detect Conan's profile
    """
    CommandExecutor(ctx)\
        .add_cwd(f"{ctx.leet_code_conan_dir}")\
        .add_command([f'conan profile detect'])\
        .execute("leet_code-conan.profile_detect.log")


@task(pre=[setup.setup_context])
@print_task_documentation
def clean(ctx):
    """
    Clean Conan's data for LeetCode
    """
    for item in os.listdir(f"{ctx.leet_code_conan_dir}"):
        item = Path(os.path.join(f"{ctx.leet_code_conan_dir}", item))
        if item.is_dir():
            if item.name.startswith('.cache'):
                shutil.rmtree(item)
                INFO.log_line(f"remove conan cache dir: {item}")
            elif item.name.startswith('.build'):
                shutil.rmtree(item)
                INFO.log_line(f"remove conan build dir: {item}")


@task(
    pre=[setup.setup_context],
    help={
        "debug": "if set configuration type will be DEBUG (else RELEASE)",
    },
)
@print_task_documentation
def install(ctx, debug=True):
    """
    Install LeetCode dependencies via Conan
    """

    build_type = "Debug" if debug else "Release"

    CommandExecutor(ctx)\
        .add_cwd(f"{ctx.leet_code_conan_dir}")\
        .add_command([
            f'conan install .',
            f'--profile conanprofile.txt',
            f'--build=missing',
            f'--settings=build_type={build_type}',
            f'--settings=compiler.runtime_type={build_type}',
            f'--core-conf=core.cache:storage_path="{ctx.leet_code_conan_dir}/.cache_{build_type}"',
            f'--core-conf=core.download:parallel=8',
            f'--output-folder="{ctx.leet_code_conan_dir}/.build_{build_type}"',
        ])\
        .execute("leet_code-conan.install.log")


collection = Collection("conan")
collection.add_task(detect_profile, name="detect-profile")
collection.add_task(clean, name="clean")
collection.add_task(install, name="install")
