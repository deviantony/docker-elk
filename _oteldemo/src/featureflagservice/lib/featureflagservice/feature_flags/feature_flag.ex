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

defmodule Featureflagservice.FeatureFlags.FeatureFlag do
  use Ecto.Schema
  import Ecto.Changeset

  schema "featureflags" do
    field :description, :string
    field :enabled, :boolean, default: false
    field :name, :string

    timestamps()
  end

  @doc false
  def changeset(feature_flag, attrs) do
    feature_flag
    |> cast(attrs, [:name, :description, :enabled])
    |> validate_required([:name, :description, :enabled])
    |> unique_constraint(:name)
  end
end
