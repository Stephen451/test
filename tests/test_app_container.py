from __future__ import annotations

from argparse import ArgumentParser
from injector import Module, provider, singleton

from pleno_common.components.component import Component
from pleno_common.infra.application import ApplicationContainer
from pleno_common.models.types import Configuration
from pleno_common.utils.exceptions import DependencyInjectionError


def test_app_container() -> None:
    """Test the application container"""

    class MyApplication(ApplicationContainer):
        def __init__(self, **kwargs) -> None:
            super().__init__(
                usage="a pleno application usage",
                description="a pleno application description",
                prog="pleno-proj",
                **kwargs,
            )

        def run(self, **kwargs):
            print("Hello World")
            return 0

    try:
        # expect failure here since we did not provide '-c' parameter
        app = MyApplication()
        app.configure(["-d", "-h"])
        app.run()
        del app
    except SystemExit:
        assert True


class MyTestComponentIncomplete(Component):
    # this is a test component that does not define a _ModuleProvider class
    # therefore it should run into issues when we try to register it via dep
    def register_configs(argparse: ArgumentParser, config: dict) -> None:
        local_config = config.get("TestComponent", {})

        Component.add_argument(
            argparse,
            "test_key",
            "TestComponent",
            default=local_config.get("test_key", "fallback_value"),
        )


class MyTestComponentInjectable(Component):
    def __init__(self, **kwargs) -> None:
        super().__init__(config_prefix="TestComponent", **kwargs)
        self.test_key = self.local_config.get("test_key")

    def register_configs(argparse: ArgumentParser, config: dict) -> None:
        local_config = config.get("TestComponent", {})

        Component.add_argument(
            argparse,
            "test_key",
            "TestComponent",
            default=local_config.get("test_key", "fallback_value"),
        )

    class _ModuleProvider(Module):
        @singleton
        @provider
        def provide_test_component_injectable(self, config: Configuration) -> MyTestComponentInjectable:
            return MyTestComponentInjectable(**config)


def test_component_config_default() -> None:
    # test that the default value declared in the TestComponent class is the default
    # in the absense of config or command line arguments
    app = ApplicationContainer(require_config=False)
    app.configure(
        [],
        additional_components=[MyTestComponentInjectable],
        foo="bar",
    )
    assert app.config["TestComponent"]["test_key"] == "fallback_value"


def test_component_config_cmdline() -> None:
    # test that the default value declared in the TestComponent class is the default
    # in the absense of config or command line arguments
    app = ApplicationContainer(require_config=False)
    # simulate user passing in python app.py --TestComponent.test_key "new_value"
    app.__init__(require_config=False)
    app.configure(
        ["--TestComponent.test_key", "new_value_from_cmdline"],
        additional_components=[MyTestComponentInjectable],
        foo="bar",
    )
    assert app.config["TestComponent"]["test_key"] == "new_value_from_cmdline"


def test_component_config_config_file() -> None:
    app = ApplicationContainer(require_config=False)

    # simulate config specified with TestCompnent section filled in
    app.__init__(require_config=False)
    app.configure(
        [],
        additional_components=[MyTestComponentInjectable],
        TestComponent={"test_key": "new_value_from_config"},
    )
    assert app.config["TestComponent"]["test_key"] == "new_value_from_config"


def test_bad_class_will_fail_di_resolution() -> None:
    app = ApplicationContainer(require_config=False)

    app.__init__(require_config=False)

    # foo=bar is an override which is required if we do not provide a config file
    try:
        app.configure([], additional_components=[MyTestComponentIncomplete], foo="bar")
        # this will fail because TestComponent does not implement `_ModuleProvider` class
        app.initialize_di()
    except DependencyInjectionError:
        assert True


def test_successful_di() -> None:
    app = ApplicationContainer(require_config=False)

    app.__init__(require_config=False)

    # foo=bar is an override which is required if we do not provide a config file
    app.configure([], additional_components=[MyTestComponentInjectable], foo="bar")
    try:
        # this will fail because TestComponent does not implement `_ModuleProvider` class
        app.initialize_di()
        obj = app.get_object(MyTestComponentInjectable)
        assert obj is not None
        assert isinstance(obj, MyTestComponentInjectable)
    except DependencyInjectionError:
        assert False
