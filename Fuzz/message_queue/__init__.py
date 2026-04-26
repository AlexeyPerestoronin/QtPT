import shutil
import invoke
import pathlib
import commandscript
import conan_task


def get_build_dir(debug=True):
    build_type = "Debug" if debug else "Release"
    return f"{commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.name}/.build_MessageQueue_{build_type}"


@commandscript.script_task()
def clean(_ctx):
    """
    Clean building data for MessageQueue.
    """
    artifacts_dir = pathlib.Path(commandscript.ENV_CONTEXT.PROJECT_ARTIFACTS_DIR.exp)
    if artifacts_dir.exists() == False:
        return

    for item in artifacts_dir.iterdir():
        item = artifacts_dir / item
        if item.is_dir():
            if item.name.startswith('.build_MessageQueue'):
                shutil.rmtree(item)
                commandscript.info.log_line(f"remove MessageQueue build dir: {item}")


@commandscript.script_task(help={
    "conan": "prepare Conan's dependencies too (by default: False)",
    "debug": "if set configuration type will be DEBUG (else RELEASE)",
})
def configure(ctx, conan: bool = False, debug: bool = True):
    """
    Configure MessageQueue.
    """

    build_type = "Debug" if debug else "Release"
    mq_dir = commandscript.ENV_CONTEXT.MESSAGE_QUEUE_DIR.name

    if conan:
        assert not conan_task.install(ctx, script_dir=ctx.script_dir, launch=ctx.launch, project_name='MessageQueue', conanfile_dir=f"{mq_dir}", debug=debug)

    commandscript.ScriptExecutor.from_ctx(ctx)\
        .add_command([
                f'cmake',
                f'-DCMAKE_BUILD_TYPE={build_type}',
                f'-DCMAKE_TOOLCHAIN_FILE="{conan_task.get_toolchain_file_path(debug, 'MessageQueue')}"',
                f'-GNinja',
                f'-S "{mq_dir}"',
                f'-B "{get_build_dir(debug)}"',
            ])\
        .execute(log="MessageQueue.configure.log")


@commandscript.script_task(
    help={
        "debug": "if set build type will be DEBUG, else RELEASE (by default DEBUG)",
        "target": "defines name of target to build (by default ALL)",
        "jobs": "defines count parallel buildings (by default 8)",
    }, )
def build(ctx, debug=True, target="all", jobs=8):
    """
    Build MessageQueue.
    """
    commandscript.ScriptExecutor.from_ctx(ctx)\
        .add_cwd(f"{get_build_dir(debug)}")\
        .add_command([f'ninja -j {jobs} {target}'])\
        .add_command([f"ninja -t compdb > compile_commands.json"])\
        .execute(log="MessageQueue.build.log")


@commandscript.script_task(
    help={
        "debug": 'if set will launch a DEBUG build of MessageQueue, otherwise - RELEASE (by default DEBUG)',
        "build_before": 'if set build before launch',
    })
def launch(ctx, debug=True, build_before: bool = True):
    """
    Launch MessageQueue.
    """
    if build_before:
        assert not build(ctx, script_dir=ctx.script_dir, launch=ctx.launch, debug=debug)

    commandscript.ScriptExecutor.from_ctx(ctx)\
        .add_cwd(f"{get_build_dir(debug)}")\
        .add_command(['./MessageQueue'])\
        .execute(log="MessageQueue.launch.log")


collection = invoke.Collection("user-input-history")
collection.add_task(clean, name="clean")
collection.add_task(configure, name="configure")
collection.add_task(build, name="build")
collection.add_task(launch, name="launch")
