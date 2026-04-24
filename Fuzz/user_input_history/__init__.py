import shutil
import invoke
import pathlib
import commandscript
import conan_task


@commandscript.script_task(help={
    "conan": "clean target Conan's files too (by default: False)",
})
def clean(ctx, conan: bool = False):
    """
    Clean building data for UserInputHistory.
    """
    uih_dir = pathlib.Path(commandscript.ENV_CONTEXT.USER_INPUT_HISTORY_DIR.exp)
    if uih_dir.exists():
        for item in uih_dir.iterdir():
            item = uih_dir / item
            if item.is_dir():
                if item.name.startswith('.cache'):
                    shutil.rmtree(item)
                    commandscript.INFO.log_line(f"remove UserInputHistory cache dir: {item}")
                elif item.name.startswith('.build'):
                    shutil.rmtree(item)
                    commandscript.INFO.log_line(f"remove UserInputHistory build dir: {item}")
    if conan:
        conan_dir = f"{commandscript.ENV_CONTEXT.USER_INPUT_HISTORY_DIR.exp}/conan"
        conan_task.clean(ctx, script_dir=ctx.script_dir, launch=ctx.launch, src=conan_dir)


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
    conan_dir = f"{commandscript.ENV_CONTEXT.USER_INPUT_HISTORY_DIR.exp}/conan"

    if conan:
        conan_task.install(ctx, script_dir=ctx.script_dir, launch=ctx.launch, src=conan_dir)

    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_command([
                f'cmake',
                f'-DCMAKE_BUILD_TYPE={build_type}',
                f'-DCMAKE_TOOLCHAIN_FILE="{conan_dir}/.build_{build_type}/build/{build_type}/generators/conan_toolchain.cmake"',
                f'-GNinja',
                f'-S "{uih_dir}"',
                f'-B "{uih_dir}/.build_{build_type}"',
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
    build_type = "Debug" if debug else "Release"
    uih_dir = commandscript.ENV_CONTEXT.USER_INPUT_HISTORY_DIR.name

    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(f"{uih_dir}/.build_{build_type}")\
        .add_command([f'ninja -j {jobs} {target}'])\
        .add_command([f"ninja -t compdb > compile_commands.json"])\
        .execute(log="UserInputHistory.build.log")


@commandscript.script_task(
    help={
        "debug": 'if set build type will be DEBUG, else RELEASE (by default DEBUG)',
        "target": 'defines regexpr-name of target to launch (by default ".+")',
        "gtest_filter": 'defines regexpr-filter for tests in targets (by default ".+")',
    }, )
def launch(ctx, debug=True, target=".+", gtest_filter="*"):
    """
    Launch UserInputHistory.
    """
    build_type = "Debug" if debug else "Release"
    uih_dir = commandscript.ENV_CONTEXT.USER_INPUT_HISTORY_DIR.name

    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(f"{uih_dir}/.build_{build_type}")\
        .add_command(['./UserInputHistory'])\
        .execute(log="UserInputHistory.launch.log")


collection = invoke.Collection("user-input-history")
collection.add_task(clean, name="clean")
collection.add_task(configure, name="configure")
collection.add_task(build, name="build")
collection.add_task(launch, name="launch")
