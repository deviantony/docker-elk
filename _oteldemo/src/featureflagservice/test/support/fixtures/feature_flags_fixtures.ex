# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

defmodule Featureflagservice.FeatureFlagsFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `Featureflagservice.FeatureFlags` context.
  """

  @doc """
  Generate a unique feature_flag name.
  """
  def unique_feature_flag_name, do: "some name#{System.unique_integer([:positive])}"

  @doc """
  Generate a feature_flag.
  """
  def feature_flag_fixture(attrs \\ %{}) do
    {:ok, feature_flag} =
      attrs
      |> Enum.into(%{
        description: "some description",
        enabled: true,
        name: unique_feature_flag_name()
      })
      |> Featureflagservice.FeatureFlags.create_feature_flag()

    feature_flag
  end
end
