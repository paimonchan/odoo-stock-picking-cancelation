# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_cancel(self):
        entries = self.filtered(lambda e: e.state != 'cancel')
        for entry in entries:
            moves = entry.move_lines
            move_lines = moves.mapped('move_line_ids')
            move_lines.write(dict(qty_done=0))
            moves.write(dict(state='cancel'))
