# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\"F\n\rServerRequest\x12\n\n\x02op\x18\x01 \x01(\t\x12\r\n\x05user1\x18\x02 \x01(\t\x12\r\n\x05user2\x18\x03 \x01(\t\x12\x0b\n\x03msg\x18\x04 \x01(\t\"-\n\x0bServerReply\x12\r\n\x05reply\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\x32\x45\n\x07\x43hatApp\x12:\n\x0ePerformService\x12\x13.chat.ServerRequest\x1a\x11.chat.ServerReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SERVERREQUEST._serialized_start=20
  _SERVERREQUEST._serialized_end=90
  _SERVERREPLY._serialized_start=92
  _SERVERREPLY._serialized_end=137
  _CHATAPP._serialized_start=139
  _CHATAPP._serialized_end=208
# @@protoc_insertion_point(module_scope)
