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

defmodule FeatureflagserviceWeb.FeatureFlagController do
  use FeatureflagserviceWeb, :controller

  alias Featureflagservice.FeatureFlags
  alias Featureflagservice.FeatureFlags.FeatureFlag

  def index(conn, _params) do
    featureflags = FeatureFlags.list_feature_flags()
    render(conn, "index.html", featureflags: featureflags)
  end

  def new(conn, _params) do
    changeset = FeatureFlags.change_feature_flag(%FeatureFlag{})
    render(conn, "new.html", changeset: changeset)
  end

  def create(conn, %{"feature_flag" => feature_flag_params}) do
    case FeatureFlags.create_feature_flag(feature_flag_params) do
      {:ok, feature_flag} ->
        conn
        |> put_flash(:info, "Feature flag created successfully.")
        |> redirect(to: Routes.feature_flag_path(conn, :show, feature_flag))

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, "new.html", changeset: changeset)
    end
  end

  def show(conn, %{"id" => id}) do
    feature_flag = FeatureFlags.get_feature_flag!(id)
    render(conn, "show.html", feature_flag: feature_flag)
  end

  def edit(conn, %{"id" => id}) do
    feature_flag = FeatureFlags.get_feature_flag!(id)
    changeset = FeatureFlags.change_feature_flag(feature_flag)
    render(conn, "edit.html", feature_flag: feature_flag, changeset: changeset)
  end

  def update(conn, %{"id" => id, "feature_flag" => feature_flag_params}) do
    feature_flag = FeatureFlags.get_feature_flag!(id)

    case FeatureFlags.update_feature_flag(feature_flag, feature_flag_params) do
      {:ok, feature_flag} ->
        conn
        |> put_flash(:info, "Feature flag updated successfully.")
        |> redirect(to: Routes.feature_flag_path(conn, :show, feature_flag))

      {:error, %Ecto.Changeset{} = changeset} ->
        render(conn, "edit.html", feature_flag: feature_flag, changeset: changeset)
    end
  end

  def delete(conn, %{"id" => id}) do
    feature_flag = FeatureFlags.get_feature_flag!(id)
    {:ok, _feature_flag} = FeatureFlags.delete_feature_flag(feature_flag)

    conn
    |> put_flash(:info, "Feature flag deleted successfully.")
    |> redirect(to: Routes.feature_flag_path(conn, :index))
  end
end
