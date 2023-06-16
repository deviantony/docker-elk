% Copyright The OpenTelemetry Authors
%
% Licensed under the Apache License, Version 2.0 (the "License");
% you may not use this file except in compliance with the License.
% You may obtain a copy of the License at
%
%     http://www.apache.org/licenses/LICENSE-2.0
%
% Unless required by applicable law or agreed to in writing, software
% distributed under the License is distributed on an "AS IS" BASIS,
% WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
% See the License for the specific language governing permissions and
% limitations under the License.

-module(ffs_service).

-behaviour(ffs_service_bhvr).

-export([get_flag/2,
         create_flag/2,
         update_flag/2,
         list_flags/2,
         delete_flag/2]).

-include_lib("grpcbox/include/grpcbox.hrl").

-include_lib("opentelemetry_api/include/otel_tracer.hrl").

-spec get_flag(ctx:t(), ffs_demo_pb:get_flag_request()) ->
    {ok, ffs_demo_pb:get_flag_response(), ctx:t()} | grpcbox_stream:grpc_error_response().
get_flag(Ctx, #{name := Name}) ->
    case 'Elixir.Featureflagservice.FeatureFlags':get_feature_flag_by_name(Name) of
        nil ->
            {grpc_error, {?GRPC_STATUS_NOT_FOUND, <<"the requested feature flag does not exist">>}};
        #{'__struct__' := 'Elixir.Featureflagservice.FeatureFlags.FeatureFlag',
          description := Description,
          enabled := Enabled,
          inserted_at := CreatedAt,
          updated_at := UpdatedAt
         } ->
            ?set_attribute('app.featureflag.name', Name),
            ?set_attribute('app.featureflag.enabled', Enabled),
            {ok, Epoch} = 'Elixir.NaiveDateTime':from_erl({{1970, 1, 1}, {0, 0, 0}}),
            CreatedAtSeconds = 'Elixir.NaiveDateTime':diff(CreatedAt, Epoch),
            UpdatedAtSeconds = 'Elixir.NaiveDateTime':diff(UpdatedAt, Epoch),
            Flag = #{name => Name,
                     description => Description,
                     enabled => Enabled,
                     created_at => #{seconds => CreatedAtSeconds, nanos => 0},
                     updated_at => #{seconds => UpdatedAtSeconds, nanos => 0}},
            {ok, #{flag => Flag}, Ctx}
    end.

-spec create_flag(ctx:t(), ffs_demo_pb:create_flag_request()) ->
    {ok, ffs_demo_pb:create_flag_response(), ctx:t()} | grpcbox_stream:grpc_error_response().
create_flag(_Ctx, _) ->
    {grpc_error, {?GRPC_STATUS_UNIMPLEMENTED, <<"use the web interface to create flags.">>}}.

-spec update_flag(ctx:t(), ffs_demo_pb:update_flag_request()) ->
    {ok, ffs_demo_pb:update_flag_response(), ctx:t()} | grpcbox_stream:grpc_error_response().
update_flag(_Ctx, _) ->
    {grpc_error, {?GRPC_STATUS_UNIMPLEMENTED, <<"use the web interface to update flags.">>}}.

-spec list_flags(ctx:t(), ffs_demo_pb:list_flags_request()) ->
    {ok, ffs_demo_pb:list_flags_response(), ctx:t()} | grpcbox_stream:grpc_error_response().
list_flags(_Ctx, _) ->
    {grpc_error, {?GRPC_STATUS_UNIMPLEMENTED, <<"use the web interface to view all flags.">>}}.

-spec delete_flag(ctx:t(), ffs_demo_pb:delete_flag_request()) ->
    {ok, ffs_demo_pb:delete_flag_response(), ctx:t()} | grpcbox_stream:grpc_error_response().
delete_flag(_Ctx, _) ->
    {grpc_error, {?GRPC_STATUS_UNIMPLEMENTED, <<"use the web interface to delete flags.">>}}.
