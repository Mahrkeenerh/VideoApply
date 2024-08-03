'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import bpy


bl_info = {
    "name" : "Video Apply",
    "author" : "Mahrkeenerh", 
    "description" : "Quick apply-all to selected video strips",
    "blender" : (4, 0, 0),
    "version" : (1, 0, 0),
    "location" : "Video Editor",
    "category" : "Sequencer"
}


class VA_OT_ApplyToSelected(bpy.types.Operator):
    bl_idname = 'video_apply.apply_to_selected'
    bl_label = 'Apply to Selected'
    bl_description = 'Apply transforms to selected video strips'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.scene.sequence_editor is None:
            return False

        return bool([strip for strip in context.scene.sequence_editor.sequences if strip.select and strip.type == 'MOVIE'])

    def execute(self, context):
        scene = context.scene
        selected = [strip for strip in scene.sequence_editor.sequences if strip.select and strip.type == 'MOVIE']

        active_strip = bpy.context.active_sequence_strip

        for strip in selected:
            if strip == active_strip:
                continue

            strip.transform.offset_x = active_strip.transform.offset_x
            strip.transform.offset_y = active_strip.transform.offset_y

            strip.transform.scale_x = active_strip.transform.scale_x
            strip.transform.scale_y = active_strip.transform.scale_y

            strip.transform.rotation = active_strip.transform.rotation

            strip.transform.origin = active_strip.transform.origin

            strip.use_flip_x = active_strip.use_flip_x
            strip.use_flip_y = active_strip.use_flip_y

        return {'FINISHED'}


class VA_OT_AutoEnd(bpy.types.Operator):
    bl_idname = 'video_apply.auto_end'
    bl_label = 'Auto End'
    bl_description = 'Automatically set the end frame of the scene to the end of the last video strip'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.scene.sequence_editor is None:
            return False

        return bool(context.scene.sequence_editor.sequences)

    def execute(self, context):
        scene = context.scene
        sequences = scene.sequence_editor.sequences

        if not sequences:
            return {'CANCELLED'}

        last_strip = sorted([strip for strip in sequences if strip.type == 'MOVIE'], key=lambda x: x.frame_final_end)[-1]

        scene.frame_end = last_strip.frame_final_end

        return {'FINISHED'}


def transforms_panel(self, context):
    op = self.layout.operator('video_apply.apply_to_selected', text='Apply to Selected')


def auto_end_panel(self, context):
    op = self.layout.operator('video_apply.auto_end', text='Auto End')


def register():
    bpy.utils.register_class(VA_OT_ApplyToSelected)
    bpy.utils.register_class(VA_OT_AutoEnd)

    bpy.types.SEQUENCER_PT_adjust_transform.append(transforms_panel)
    bpy.types.DOPESHEET_HT_header.append(auto_end_panel)


def unregister():
    bpy.utils.unregister_class(VA_OT_ApplyToSelected)
    bpy.utils.unregister_class(VA_OT_AutoEnd)

    bpy.types.SEQUENCER_PT_adjust_transform.remove(transforms_panel)
    bpy.types.DOPESHEET_HT_header.remove(auto_end_panel)
