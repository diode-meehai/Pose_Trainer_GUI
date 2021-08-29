# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/refine_landmarks_from_heatmap_calculator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/calculators/util/refine_landmarks_from_heatmap_calculator.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\nImediapipe/calculators/util/refine_landmarks_from_heatmap_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xd3\x01\n+RefineLandmarksFromHeatmapCalculatorOptions\x12\x16\n\x0bkernel_size\x18\x01 \x01(\x05:\x01\x39\x12%\n\x18min_confidence_to_refine\x18\x02 \x01(\x02:\x03\x30.52e\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xb5\xf5\xdf\xac\x01 \x01(\x0b\x32\x36.mediapipe.RefineLandmarksFromHeatmapCalculatorOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_REFINELANDMARKSFROMHEATMAPCALCULATOROPTIONS = _descriptor.Descriptor(
  name='RefineLandmarksFromHeatmapCalculatorOptions',
  full_name='mediapipe.RefineLandmarksFromHeatmapCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='kernel_size', full_name='mediapipe.RefineLandmarksFromHeatmapCalculatorOptions.kernel_size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=9,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_confidence_to_refine', full_name='mediapipe.RefineLandmarksFromHeatmapCalculatorOptions.min_confidence_to_refine', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.RefineLandmarksFromHeatmapCalculatorOptions.ext', index=0,
      number=362281653, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=127,
  serialized_end=338,
)

DESCRIPTOR.message_types_by_name['RefineLandmarksFromHeatmapCalculatorOptions'] = _REFINELANDMARKSFROMHEATMAPCALCULATOROPTIONS

RefineLandmarksFromHeatmapCalculatorOptions = _reflection.GeneratedProtocolMessageType('RefineLandmarksFromHeatmapCalculatorOptions', (_message.Message,), dict(
  DESCRIPTOR = _REFINELANDMARKSFROMHEATMAPCALCULATOROPTIONS,
  __module__ = 'mediapipe.calculators.util.refine_landmarks_from_heatmap_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.RefineLandmarksFromHeatmapCalculatorOptions)
  ))
_sym_db.RegisterMessage(RefineLandmarksFromHeatmapCalculatorOptions)

_REFINELANDMARKSFROMHEATMAPCALCULATOROPTIONS.extensions_by_name['ext'].message_type = _REFINELANDMARKSFROMHEATMAPCALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_REFINELANDMARKSFROMHEATMAPCALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)