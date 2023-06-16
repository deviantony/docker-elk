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

defmodule FeatureflagserviceWeb.FeatureFlagControllerTest do
  use FeatureflagserviceWeb.ConnCase

  import Featureflagservice.FeatureFlagsFixtures

  @create_attrs %{description: "some description", enabled: true, name: "some name"}
  @update_attrs %{
    description: "some updated description",
    enabled: false,
    name: "some updated name"
  }
  @invalid_attrs %{description: nil, enabled: nil, name: nil}

  describe "index" do
    test "lists all featureflags", %{conn: conn} do
      conn = get(conn, Routes.feature_flag_path(conn, :index))
      assert html_response(conn, 200) =~ "Listing feature flags"
    end
  end

  describe "new feature_flag" do
    test "renders form", %{conn: conn} do
      conn = get(conn, Routes.feature_flag_path(conn, :new))
      assert html_response(conn, 200) =~ "New Feature flag"
    end
  end

  describe "create feature_flag" do
    test "redirects to show when data is valid", %{conn: conn} do
      conn = post(conn, Routes.feature_flag_path(conn, :create), feature_flag: @create_attrs)

      assert %{id: id} = redirected_params(conn)
      assert redirected_to(conn) == Routes.feature_flag_path(conn, :show, id)

      conn = get(conn, Routes.feature_flag_path(conn, :show, id))
      assert html_response(conn, 200) =~ "Show feature flag"
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, Routes.feature_flag_path(conn, :create), feature_flag: @invalid_attrs)
      assert html_response(conn, 200) =~ "New feature flag"
    end
  end

  describe "edit feature_flag" do
    setup [:create_feature_flag]

    test "renders form for editing chosen feature_flag", %{conn: conn, feature_flag: feature_flag} do
      conn = get(conn, Routes.feature_flag_path(conn, :edit, feature_flag))
      assert html_response(conn, 200) =~ "Edit feature flag"
    end
  end

  describe "update feature_flag" do
    setup [:create_feature_flag]

    test "redirects when data is valid", %{conn: conn, feature_flag: feature_flag} do
      conn =
        put(conn, Routes.feature_flag_path(conn, :update, feature_flag),
          feature_flag: @update_attrs
        )

      assert redirected_to(conn) == Routes.feature_flag_path(conn, :show, feature_flag)

      conn = get(conn, Routes.feature_flag_path(conn, :show, feature_flag))
      assert html_response(conn, 200) =~ "some updated description"
    end

    test "renders errors when data is invalid", %{conn: conn, feature_flag: feature_flag} do
      conn =
        put(conn, Routes.feature_flag_path(conn, :update, feature_flag),
          feature_flag: @invalid_attrs
        )

      assert html_response(conn, 200) =~ "Edit feature flag"
    end
  end

  describe "delete feature_flag" do
    setup [:create_feature_flag]

    test "deletes chosen feature_flag", %{conn: conn, feature_flag: feature_flag} do
      conn = delete(conn, Routes.feature_flag_path(conn, :delete, feature_flag))
      assert redirected_to(conn) == Routes.feature_flag_path(conn, :index)

      assert_error_sent 404, fn ->
        get(conn, Routes.feature_flag_path(conn, :show, feature_flag))
      end
    end
  end

  defp create_feature_flag(_) do
    feature_flag = feature_flag_fixture()
    %{feature_flag: feature_flag}
  end
end
