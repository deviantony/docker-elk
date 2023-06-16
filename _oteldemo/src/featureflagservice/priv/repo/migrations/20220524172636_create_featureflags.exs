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

defmodule Featureflagservice.Repo.Migrations.CreateFeatureflags do
  use Ecto.Migration

  def change do
    create table(:featureflags) do
      add :name, :string
      add :description, :string
      add :enabled, :boolean, default: false, null: false

      timestamps()
    end

    create unique_index(:featureflags, [:name])

    execute(&execute_up/0, &execute_down/0)
  end

  defp execute_up do
    repo().insert(%Featureflagservice.FeatureFlags.FeatureFlag{
      name: "productCatalogFailure",
      description: "Fail product catalog service on a specific product",
      enabled: false})

    repo().insert(%Featureflagservice.FeatureFlags.FeatureFlag{
      name: "recommendationCache",
      description: "Cache recommendations",
      enabled: false})

    repo().insert(%Featureflagservice.FeatureFlags.FeatureFlag{
      name: "adServiceFailure",
      description: "Fail ad service requests sporadically",
      enabled: false})
  end

  defp execute_down do
    repo().delete(%Featureflagservice.FeatureFlags.FeatureFlag{name: "productCatalogFailure"})
    repo().delete(%Featureflagservice.FeatureFlags.FeatureFlag{name: "recommendationCache"})
    repo().delete(%Featureflagservice.FeatureFlags.FeatureFlag{name: "adServiceFailure"})
  end
end
