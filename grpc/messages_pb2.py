# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emessages.proto\";\n\x07\x41\x63\x63ount\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\x08loggedIn\x18\x02 \x01(\x08H\x00\x88\x01\x01\x42\x0b\n\t_loggedIn\"\x1e\n\x0e\x41\x63\x63ountRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"?\n\x0f\x41\x63\x63ountResponse\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x15\n\rresponse_text\x18\x02 \x01(\t\"\x15\n\x13ListAccountsRequest\"2\n\x14ListAccountsResponse\x12\x1a\n\x08\x61\x63\x63ounts\x18\x01 \x03(\x0b\x32\x08.Account2\x99\x02\n\x0fMessageExchange\x12\x34\n\rCreateAccount\x12\x0f.AccountRequest\x1a\x10.AccountResponse\"\x00\x12,\n\x05LogIn\x12\x0f.AccountRequest\x1a\x10.AccountResponse\"\x00\x12=\n\x0cListAccounts\x12\x14.ListAccountsRequest\x1a\x15.ListAccountsResponse\"\x00\x12-\n\x06LogOut\x12\x0f.AccountRequest\x1a\x10.AccountResponse\"\x00\x12\x34\n\rDeleteAccount\x12\x0f.AccountRequest\x1a\x10.AccountResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACCOUNT._serialized_start=18
  _ACCOUNT._serialized_end=77
  _ACCOUNTREQUEST._serialized_start=79
  _ACCOUNTREQUEST._serialized_end=109
  _ACCOUNTRESPONSE._serialized_start=111
  _ACCOUNTRESPONSE._serialized_end=174
  _LISTACCOUNTSREQUEST._serialized_start=176
  _LISTACCOUNTSREQUEST._serialized_end=197
  _LISTACCOUNTSRESPONSE._serialized_start=199
  _LISTACCOUNTSRESPONSE._serialized_end=249
  _MESSAGEEXCHANGE._serialized_start=252
  _MESSAGEEXCHANGE._serialized_end=533
# @@protoc_insertion_point(module_scope)
