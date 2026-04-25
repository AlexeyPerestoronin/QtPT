import shutil
import invoke
import pathlib
import commandscript
import conan_task


def get_build_dir(debug=True):
    build_type = "Debug" if debug else "Release"
    return f"{commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.name}/.build_UserInputHistory_{build_type}"


@commandscript.script_task()
def clean(_ctx):
    """
    Clean building data for UserInputHistory.
    """
    artifacts_dir = pathlib.Path(commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.exp)
    if artifacts_dir.exists() == False:
        return

    for item in artifacts_dir.iterdir():
        item = artifacts_dir / item
        if item.is_dir():
            if item.name.startswith('.build_UserInputHistory'):
                shutil.rmtree(item)
                commandscript.INFO.log_line(f"remove UserInputHistory build dir: {item}")


@commandscript.script_task(help={
    "conan": "prepare Conan's dependencies too (by default: False)",
    "debug": "if set configuration type will be DEBUG (else RELEASE)",
})
def configure(ctx, conan: bool = False, debug: bool = True):
    """
    Configure UserInputHistory.
    """

    build_type = "Debug" if debug else "Release"
    uih_dir = commandscript.ENV_CONTEXT.USER_INPUT_HISTORY_DIR.name

    if conan:
        conan_task.install(ctx, script_dir=ctx.script_dir, launch=ctx.launch, profile_path=f"{uih_dir}/conan", debug=debug)

    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_command([
                f'cmake',
                f'-DCMAKE_BUILD_TYPE={build_type}',
                f'-DCMAKE_TOOLCHAIN_FILE="{conan_task.get_toolchain_file_path(debug)}"',
                f'-GNinja',
                f'-S "{uih_dir}"',
                f'-B "{get_build_dir(debug)}"',
            ])\
        .execute(log="UserInputHistory.configure.log")


@commandscript.script_task(
    help={
        "debug": "if set build type will be DEBUG, else RELEASE (by default DEBUG)",
        "target": "defines name of target to build (by default ALL)",
        "jobs": "defines count parallel buildings (by default 8)",
    }, )
def build(ctx, debug=True, target="all", jobs=8):
    """
    Build UserInputHistory.
    """
    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(f"{get_build_dir(debug)}")\
        .add_command([f'ninja -j {jobs} {target}'])\
        .add_command([f"ninja -t compdb > compile_commands.json"])\
        .execute(log="UserInputHistory.build.log")


@commandscript.script_task(help={
    "debug": 'if set build type will be DEBUG, else RELEASE (by default DEBUG)',
})
def launch(ctx, debug=True):
    """
    Launch UserInputHistory.
    """
    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(f"{get_build_dir(debug)}")\
        .add_command(['echo $LD_LIBRARY_PATH'])\
        .add_command(['ldd ./UserInputHistory'])\
        .add_command(['./UserInputHistory'])\
        .execute(log="UserInputHistory.launch.log")


collection = invoke.Collection("user-input-history")
collection.add_task(clean, name="clean")
collection.add_task(configure, name="configure")
collection.add_task(build, name="build")
collection.add_task(launch, name="launch")
