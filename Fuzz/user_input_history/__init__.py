import shutil
import invoke
import pathlib
import commandscript

@commandscript.script_task()
def clean(ctx):
    """
    Clean building data for UserInputHistory.
    """
    uih_dir = pathlib.Path(commandscript.ENV_CONTEXT.USER_INPUT_HISTORY_DIR.exp)
    if uih_dir.exists() == False:
        return

    for item in uih_dir.iterdir():
        item = uih_dir / item
        if item.is_dir():
            if item.name.startswith('.cache'):
                shutil.rmtree(item)
                commandscript.INFO.log_line(f"remove UserInputHistory cache dir: {item}")
            elif item.name.startswith('.build'):
                shutil.rmtree(item)
                commandscript.INFO.log_line(f"remove UserInputHistory build dir: {item}")


@commandscript.script_task(
    help={
        "debug": "if set configuration type will be DEBUG (else RELEASE)",
    },
)
def configure(ctx, debug=True):
    """
    Configure UserInputHistory.
    """

    build_type = "Debug" if debug else "Release"
    conan_dir = commandscript.ENV_CONTEXT.PROJECT_CONAN_DIR.name
    uih_dir = commandscript.ENV_CONTEXT.USER_INPUT_HISTORY_DIR.name

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
    },
)
def build(ctx, debug=True, target="all", jobs=8):
    """
    Build LeetCode-project
    """

    build_type = "Debug" if debug else "Release"

    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(f"{ctx.leet_code_cmake_dir}/.build_{build_type}")\
        .add_command([
            f'ninja',
            f'-j {jobs}',
            f'{target}',
        ], enter=False)\
        .execute(log="UserInputHistory.build.log")


@commandscript.script_task(
    help={
        "debug": 'if set build type will be DEBUG, else RELEASE (by default DEBUG)',
        "target": 'defines regexpr-name of target to launch (by default ".+")',
        "gtest_filter": 'defines regexpr-filter for tests in targets (by default ".+")',
    },
)
def launch(ctx, debug=True, target=".+", gtest_filter="*"):
    """
    Launch targets of LeetCode-project
    """

    build_type = "Debug" if debug else "Release"
    targets_dir = f"{ctx.leet_code_cmake_dir}/.build_{build_type}"

    commands = []
    for item in os.listdir(f"{targets_dir}"):
        item = Path(os.path.join(f"{targets_dir}", item))
        if item.is_file():
            if item.name.endswith('.exe'):
                if re.match(target, item.name):
                    INFO.log_line(f'detected by "{target}": {item.name}')
                    commands.append([f'{item.name} --gtest_filter="{gtest_filter}"'])

    commandscript.ScriptExecutor(ctx.script_dir, ctx.launch)\
        .add_cwd(f"{targets_dir}")\
        .add_commands(commands)\
        .execute("UserInputHistory.launch.log")


collection = invoke.Collection("user-input-history")
collection.add_task(clean, name="clean")
collection.add_task(configure, name="configure")
collection.add_task(build, name="build")
collection.add_task(launch, name="launch")
