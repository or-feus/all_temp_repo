import pytest
from unittest import mock

m = mock.Mock()
m.some_method.return_value = "Hello world"

print(m.some_method(1, 4, 5, 6))