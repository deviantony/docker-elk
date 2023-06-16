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

defmodule Featureflagservice.FeatureFlagsTest do
  use Featureflagservice.DataCase

  alias Featureflagservice.FeatureFlags

  describe "featureflags" do
    alias Featureflagservice.FeatureFlags.FeatureFlag

    import Featureflagservice.FeatureFlagsFixtures

    @invalid_attrs %{description: nil, enabled: nil, name: nil}

    test "list_feature_flags/0 returns all featureflags" do
      feature_flag = feature_flag_fixture()
      assert FeatureFlags.list_feature_flags() == [feature_flag]
    end

    test "get_feature_flag!/1 returns the feature_flag with given id" do
      feature_flag = feature_flag_fixture()
      assert FeatureFlags.get_feature_flag!(feature_flag.id) == feature_flag
    end

    test "create_feature_flag/1 with valid data creates a feature_flag" do
      valid_attrs = %{description: "some description", enabled: true, name: "some name"}

      assert {:ok, %FeatureFlag{} = feature_flag} = FeatureFlags.create_feature_flag(valid_attrs)
      assert feature_flag.description == "some description"
      assert feature_flag.enabled == true
      assert feature_flag.name == "some name"
    end

    test "create_feature_flag/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = FeatureFlags.create_feature_flag(@invalid_attrs)
    end

    test "update_feature_flag/2 with valid data updates the feature_flag" do
      feature_flag = feature_flag_fixture()

      update_attrs = %{
        description: "some updated description",
        enabled: false,
        name: "some updated name"
      }

      assert {:ok, %FeatureFlag{} = feature_flag} =
               FeatureFlags.update_feature_flag(feature_flag, update_attrs)

      assert feature_flag.description == "some updated description"
      assert feature_flag.enabled == false
      assert feature_flag.name == "some updated name"
    end

    test "update_feature_flag/2 with invalid data returns error changeset" do
      feature_flag = feature_flag_fixture()

      assert {:error, %Ecto.Changeset{}} =
               FeatureFlags.update_feature_flag(feature_flag, @invalid_attrs)

      assert feature_flag == FeatureFlags.get_feature_flag!(feature_flag.id)
    end

    test "delete_feature_flag/1 deletes the feature_flag" do
      feature_flag = feature_flag_fixture()
      assert {:ok, %FeatureFlag{}} = FeatureFlags.delete_feature_flag(feature_flag)
      assert_raise Ecto.NoResultsError, fn -> FeatureFlags.get_feature_flag!(feature_flag.id) end
    end

    test "change_feature_flag/1 returns a feature_flag changeset" do
      feature_flag = feature_flag_fixture()
      assert %Ecto.Changeset{} = FeatureFlags.change_feature_flag(feature_flag)
    end
  end
end
