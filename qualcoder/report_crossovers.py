# -*- coding: utf-8 -*-

"""
Copyright (c) 2020 Colin Curtain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Author: Colin Curtain (ccbogel)
https://github.com/ccbogel/QualCoder
https://qualcoder.wordpress.com/
"""

from copy import copy
import datetime
import logging
import os
import sys
import traceback

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush

from GUI.ui_dialog_code_crossovers import Ui_Dialog_CodeCrossovers
from select_items import DialogSelectItems

path = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger(__name__)


def exception_handler(exception_type, value, tb_obj):
    """ Global exception handler useful in GUIs.
    tb_obj: exception.__traceback__ """
    tb = '\n'.join(traceback.format_tb(tb_obj))
    text = 'Traceback (most recent call last):\n' + tb + '\n' + exception_type.__name__ + ': ' + str(value)
    print(text)
    logger.error(_("Uncaught exception: ") + text)
    QtWidgets.QMessageBox.critical(None, _('Uncaught Exception'), text)


class DialogReportCrossovers(QtWidgets.QDialog):
    """ Show code relations/crossovers for one coder.
    This is for text only. """

    app = None
    dialog_list = None
    parent_textEdit = None
    categories = []
    codes = []
    result_relations = []

    def __init__(self, app, parent_textEdit, dialog_list):

        sys.excepthook = exception_handler
        self.app = app
        self.dialog_list = dialog_list
        self.parent_textEdit = parent_textEdit
        self.get_code_data()
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_Dialog_CodeCrossovers()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        try:
            w = int(self.app.settings['dialogcodecrossovers_w'])
            h = int(self.app.settings['dialogcodecrossovers_h'])
            if h > 50 and w > 50:
                self.resize(w, h)
            s0 = int(self.app.settings['dialogcodecrossovers_splitter0'])
            s1 = int(self.app.settings['dialogcodecrossovers_splitter1'])
            if s0 > 10 and s1 > 10:
                self.ui.splitter.setSizes([s0, s1])
        except:
            pass
        font = 'font: ' + str(self.app.settings['fontsize']) + 'pt '
        font += '"' + self.app.settings['font'] + '";'
        self.setStyleSheet(font)
        font = 'font: ' + str(self.app.settings['treefontsize']) + 'pt '
        font += '"' + self.app.settings['font'] + '";'
        self.ui.treeWidget.setStyleSheet(font)
        self.ui.treeWidget.setSelectionMode(QtWidgets.QTreeWidget.ExtendedSelection)
        self.fill_tree()
        self.ui.pushButton_exportcsv.pressed.connect(self.export_csv_file)
        self.ui.pushButton_exportcsv.setEnabled(False)  # tmp
        self.ui.pushButton_calculate.pressed.connect(self.calculate_crossovers)

    def get_code_data(self):
        """ Called from init. gets code_names and categories.
        """
        #TODO use App method ?

        cur = self.app.conn.cursor()
        self.categories = []
        cur.execute("select name, catid, owner, date, memo, supercatid from code_cat order by lower(name)")
        result = cur.fetchall()
        for row in result:
            self.categories.append({'name': row[0], 'catid': row[1], 'owner': row[2],
            'date': row[3], 'memo': row[4], 'supercatid': row[5],
            'display_list': [row[0], 'catid:' + str(row[1])]})
        self.codes = []
        cur.execute("select name, memo, owner, date, cid, catid, color from code_name order by lower(name)")
        result = cur.fetchall()
        for row in result:
            self.codes.append({'name': row[0], 'memo': row[1], 'owner': row[2], 'date': row[3],
            'cid': row[4], 'catid': row[5], 'color': row[6],
            'display_list': [row[0], 'cid:' + str(row[4])]})

    def calculate_crossovers(self):
        """ Calculate the crossovers for selected codes for THIS coder.
        For codings in code_text only.

        id1, id2, overlapindex, unionindex, distance, whichmin, whichmax, fid
        relation is 1 character: Inclusion, Overlap, Exact, Proximity
        """

        sel_codes = []
        codes_str = ""
        code_ids = ""
        items = self.ui.treeWidget.selectedItems()
        for i in items:
            if i.text(1)[:3] == "cid":
                sel_codes.append({"name": i.text(0), "cid": int(i.text(1)[4:])})
                codes_str += i.text(0) + "|"
                code_ids += "," + i.text(1)[4:]
        if len(sel_codes) < 2:
            mb = QtWidgets.QMessageBox()
            mb.setIcon(QtWidgets.QMessageBox.Warning)
            mb.setStyleSheet("* {font-size:" + str(self.app.settings['fontsize']) + "pt} ")
            mb.setWindowTitle(_('Selection warning'))
            msg = _("Select 2 or more codes\nUse Ctrl or Shift and mouse click")
            mb.setText(msg)
            mb.exec_()
            return

        code_ids = code_ids[1:]
        self.ui.label_codes.setText(_("Codes: ") + codes_str)

        cur = self.app.conn.cursor()
        sql = "select distinct fid from code_text where owner=? and code_text.cid in (" + code_ids + ") \
            order by fid"
        cur.execute(sql, [self.app.settings['codername'], ])
        result = cur.fetchall()
        file_ids = []
        file_ids_str = ""
        for r in result:
            file_ids.append(r[0])
            file_ids_str += "," + str(r[0])

        if file_ids == []:
            mb = QtWidgets.QMessageBox()
            mb.setIcon(QtWidgets.QMessageBox.Warning)
            mb.setStyleSheet("* {font-size:" + str(self.app.settings['fontsize']) + "pt} ")
            mb.setWindowTitle(_('Selection warning'))
            msg = _("There are no files containing this combination of codes")
            mb.setText(msg)
            mb.exec_()
            return

        # To add file names to relation result - makes easier for diplaying results
        file_ids_str = file_ids_str[1:]
        sql = "select distinct id, name from source where id in (" + file_ids_str + ")"
        cur.execute(sql)
        file_id_names = cur.fetchall()
        #print(file_id_names)

        # Need to look at each text file separately,
        # only look at current coder
        self.result_relations = []
        for fid in file_ids:
            filename = ""
            for f in file_id_names:
                if f[0] == fid:
                    filename = f[1]

            sql = "select fid, code_text.cid, pos0, pos1, name from code_text join code_name on \
             code_name.cid=code_text.cid where code_text.owner=? and fid=? \
             and code_text.cid in (" + code_ids + ") \
            order by code_text.cid"
            cur.execute(sql, [self.app.settings['codername'], fid])
            result = cur.fetchall()
            coded = []
            for row in result:
                if row[0] in file_ids or file_ids == []:
                    coded.append(row)

            #TODO later, find the closest Other code for relation analysis
            # Look at each code again other codes, when done remove from list of codes
            # Sort results in result_relations for display and export
            CID = 1
            POS0 = 2
            POS1 = 3
            NAME = 4
            while len(coded) > 0:
                c0 = coded.pop()
                for c1 in coded:
                    if c0[CID] != c1[CID]:
                        #print(c0, c1)
                        relation = self.relation(c0, c1)
                        # Add extra details for output
                        relation['c0_name'] = c0[NAME]
                        relation['c1_name'] = c1[NAME]
                        relation['fid'] = fid
                        relation['file_name'] = filename
                        relation['c0_pos0'] = c0[POS0]
                        relation['c0_pos1'] = c0[POS1]
                        relation['c1_pos0'] = c1[POS0]
                        relation['c1_pos1'] = c1[POS1]
                        self.result_relations.append(relation)
                        #print(relation)
        self.display_relations()

    def closest_relation(self, c0, c1):
        #TODO later
        pass

    def relation(self, c0, c1):
        """ Relation function as in RQDA

        whichmin is the code with the lowest pos0, or None if equal
        whichmax is the code with the highest pos1 or None if equal
        operlapindex is the combined lowest to highest positions. Only used for E, O, P
        unionindex is the lowest and highest positions of the union of overlap. Only used for E, O

        Returns:
        id1, id2, overlapindex, unionindex, distance, whichmin, whichmax, fid
        relation is 1 character: Inclusion, Overlap, Exact, Proximity
        """

        CID = 1
        POS0 = 2
        POS1 = 3
        result = {"cid0": c0[CID], "cid1": c1[CID], "relation": "", "whichmin": None, "whichmax": None,
            "overlapindex": None, "unionindex": None, "distance": None}

        # whichmin
        if c0[POS0] < c1[POS0]:
            result['whichmin'] = c0[CID]
        if c1[POS0] < c0[POS0]:
            result['whichmin'] = c1[CID]

        # whichmax
        if c0[POS1] > c1[POS1]:
            result['whichmax'] = c0[CID]
        if c1[POS1] > c0[POS1]:
            result['whichmax'] = c1[CID]

        # Check for Exact
        if c0[POS0] == c1[POS0] and c0[POS1] == c1[POS1]:
            result['relation'] = "E"
            result['overlapindex'] = [c0[POS0], c0[POS1]]
            result['unionindex'] = [c0[POS0], c0[POS1]]
            return result

        # Check for Proximity
        if c0[POS1] < c1[POS0]:
            result['relation'] = "P"
            result['distance'] = c1[POS0] - c0[POS1]
            return result
        if c0[POS0] > c1[POS1]:
            result['relation'] = "P"
            result['distance'] = c0[POS0] - c1[POS1]
            return result

        # Check for Inclusion
        # Note Exact has been resolved already
        # c0 inside c1
        if c0[POS0] >= c1[POS0] and c0[POS1] <= c1[POS1]:
            result['relation'] = "I"
            result['overlapindex'] = [c0[POS0], c0[POS1]]
            result['unionindex'] = [c0[POS0], c0[POS1]]
            return result
        # c1 inside c0
        if c1[POS0] >= c0[POS0] and c1[POS1] <= c0[POS1]:
            result['relation'] = "I"
            result['overlapindex'] = [c1[POS0], c1[POS1]]
            result['unionindex'] = [c1[POS0], c1[POS1]]
            return result

        # Check for Overlap
        # Should be all that is remaining
        # c0 overlaps from the right, left is not overlapping
        if c0[POS0] < c1[POS0] and c0[POS1] < c1[POS1]:
            result['relation'] = "O"
            # Reorder lowest to highest
            result['overlapindex'] = [c0[POS0], c1[POS1]].sort()
            result['unionindex'] = [c0[POS1], c1[POS0]].sort()
            return result

        # c1 overlaps from the right, left is not overlapping
        if c1[POS0] < c0[POS0] and c1[POS1] < c0[POS1]:
            result['relation'] = "O"
            result['overlapindex'] = [c1[POS0], c0[POS1]].sort()
            result['unionindex'] = [c1[POS1], c0[POS0]].sort()
            return result

    def display_relations(self):
        """ Perhaps as table of:
        Tooltips with codenames on id1,id2, relation,fid
        id1, id2, overlapindex, unionindex, distance, whichmin, whichmax, fid
        relation is: inclusion, overlap, exact, proximity
        """

        FID = 0
        C0 = 1
        C1 = 2
        REL = 3
        MIN = 4
        MAX = 5
        O0 = 6
        O1 = 7
        U0 = 8
        U1 = 9
        DIST = 10

        col_names = ["FID", "Code0", "Code1", "Rel", "Min", "Max", "Overlap0", "Overlap1", "Union0", "Union1", "Distance"]
        self.ui.tableWidget.setColumnCount(len(col_names))
        self.ui.tableWidget.setHorizontalHeaderLabels(col_names)
        rows = self.ui.tableWidget.rowCount()
        for r in range(0, rows):
            self.ui.tableWidget.removeRow(0)
        for r, i in enumerate(self.result_relations):
            self.ui.tableWidget.insertRow(r)
            item = QtWidgets.QTableWidgetItem(str(i['fid']))
            #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setToolTip(i['file_name'])
            self.ui.tableWidget.setItem(r, FID, item)

            item = QtWidgets.QTableWidgetItem(str(i['cid0']))
            #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setToolTip(i['c0_name'] + "\n" + str(i['c0_pos0']) + " - " + str(i['c0_pos1']))
            self.ui.tableWidget.setItem(r, C0, item)

            item = QtWidgets.QTableWidgetItem(str(i['cid1']))
            #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            item.setToolTip(i['c1_name'] + "\n" + str(i['c1_pos0']) + " - " + str(i['c1_pos1']))
            self.ui.tableWidget.setItem(r, C1, item)

            item = QtWidgets.QTableWidgetItem(str(i['relation']))
            #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            ttip = _("Proximity")
            if i['relation'] == "O":
                ttip = _("Overlap")
            if i['relation'] == "E":
                ttip = _("Exact")
            if i['relation'] == "I":
                ttip = _("Inclusion")
            item.setToolTip(ttip)
            self.ui.tableWidget.setItem(r, REL, item)

            item = QtWidgets.QTableWidgetItem(str(i['whichmin']).replace("None", ""))
            #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            if i['whichmin'] is not None:
                ttip = i['c0_name']
                if i['whichmin'] == i['cid1']:
                    ttip = i['c1_name']
                item.setToolTip(ttip)
            self.ui.tableWidget.setItem(r, MIN, item)

            item = QtWidgets.QTableWidgetItem(str(i['whichmax']).replace("None", ""))
            #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            if i['whichmax'] is not None:
                ttip = i['c0_name']
                if i['whichmax'] == i['cid1']:
                    ttip = i['c1_name']
                item.setToolTip(ttip)
            self.ui.tableWidget.setItem(r, MAX, item)

            if i['overlapindex'] is not None:
                item = QtWidgets.QTableWidgetItem(str(i['overlapindex'][0]))
                #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.tableWidget.setItem(r,O0, item)
                item = QtWidgets.QTableWidgetItem(str(i['overlapindex'][1]))
                # item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.tableWidget.setItem(r, O1, item)

            if i['unionindex'] is not None:
                item = QtWidgets.QTableWidgetItem(str(i['unionindex'][0]))
                # item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.tableWidget.setItem(r, U0, item)
                item = QtWidgets.QTableWidgetItem(str(i['unionindex'][1]))
                #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.ui.tableWidget.setItem(r, U1, item)

            item = QtWidgets.QTableWidgetItem(str(i['distance']).replace("None", ""))
            #item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.ui.tableWidget.setItem(r, DIST, item)

        self.ui.tableWidget.resizeColumnsToContents()

    def fill_tree(self):
        """ Fill tree widget, top level items are main categories and unlinked codes.
        """

        self.ui.treeWidget.clear()

        cats = copy(self.categories)
        codes = copy(self.codes)
        self.ui.treeWidget.clear()
        header = [_("Code Tree"), "Id"]
        self.ui.treeWidget.setColumnCount(len(header))
        self.ui.treeWidget.setHeaderLabels(header)
        if self.app.settings['showids'] == 'False':
            self.ui.treeWidget.setColumnHidden(1, True)
        else:
            self.ui.treeWidget.setColumnHidden(1, False)
        self.ui.treeWidget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ui.treeWidget.header().setStretchLastSection(False)
        # add top level categories
        remove_list = []
        for c in cats:
            if c['supercatid'] is None:
                display_list = []
                for i in c['display_list']:
                    display_list.append(str(i))
                top_item = QtWidgets.QTreeWidgetItem(display_list)
                self.ui.treeWidget.addTopLevelItem(top_item)
                remove_list.append(c)
        for item in remove_list:
            #try:
            cats.remove(item)
            #except Exception as e:
            #    logger.debug(str(e) + " item:" + str(item))

        ''' Add child categories. Look at each unmatched category, iterate through tree to
        add as child then remove matched categories from the list. '''
        count = 0
        while len(cats) > 0 or count < 10000:
            remove_list = []
            #logger.debug("cats:" + str(cats))
            for c in cats:
                it = QtWidgets.QTreeWidgetItemIterator(self.ui.treeWidget)
                item = it.value()
                while item:  # while there is an item in the list
                    #logger.debug("While: ", item.text(0), item.text(1), c['catid'], c['supercatid'])
                    if item.text(1) == 'catid:' + str(c['supercatid']):
                        display_list = []
                        for i in c['display_list']:
                            display_list.append(str(i))
                        child = QtWidgets.QTreeWidgetItem(display_list)
                        item.addChild(child)
                        #logger.debug("Adding: " + c['name'])
                        remove_list.append(c)
                    it += 1
                    item = it.value()
            for item in remove_list:
                cats.remove(item)
            count += 1

        # add unlinked codes as top level items
        remove_items = []
        for c in codes:
            if c['catid'] is None:
                #logger.debug("c[catid] is None: new top item c[name]:" + c['name'])
                display_list = []
                for i in c['display_list']:
                    display_list.append(str(i))
                top_item = QtWidgets.QTreeWidgetItem(display_list)
                top_item.setBackground(0, QBrush(QtGui.QColor(c['color']), Qt.SolidPattern))
                top_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                self.ui.treeWidget.addTopLevelItem(top_item)
                remove_items.append(c)
        for item in remove_items:
            codes.remove(item)

        # add codes as children
        for c in codes:
            it = QtWidgets.QTreeWidgetItemIterator(self.ui.treeWidget)
            item = it.value()
            while item:
                #logger.debug("for c in codes, item:" + item.text(0) +"|" + item.text(1) + ", c[cid]:" + str(c['cid']) +", c[catid]:" + str(c['catid']))
                if item.text(1) == 'catid:' + str(c['catid']):
                    display_list = []
                    for i in c['display_list']:
                        display_list.append(str(i))
                    child = QtWidgets.QTreeWidgetItem(display_list)
                    child.setBackground(0, QBrush(QtGui.QColor(c['color']), Qt.SolidPattern))
                    child.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    item.addChild(child)
                    c['catid'] = -1  # make unmatchable
                it += 1
                item = it.value()
        self.ui.treeWidget.expandAll()

    def export_csv_file(self):
        """ Export data as csv. """

        return

        '''shortname = self.app.project_name.split(".qda")[0]
        filename = shortname + " code frequencies.csv"
        options = QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly
        directory = QtWidgets.QFileDialog.getExistingDirectory(None,
            _("Select directory to save file"), self.app.last_export_directory, options)
        if directory == "":
            return
        if directory != self.app.last_export_directory:
            self.app.last_export_directory = directory
        filename = directory + "/" + filename
        if os.path.exists(filename):
            mb = QtWidgets.QMessageBox()
            mb.setWindowTitle(_("File exists"))
            mb.setText(_("Overwrite?"))
            mb.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            mb.setStyleSheet("* {font-size:" + str(self.app.settings['fontsize']) + "pt} ")
            if mb.exec_() == QtWidgets.QMessageBox.No:
                return
        data = ""
        header = [_("Code Tree"), "Id"]
        for coder in self.coders:
            header.append(coder)
        header.append("Total")
        data += ",".join(header) + "\n"

        it = QtWidgets.QTreeWidgetItemIterator(self.ui.treeWidget)
        item = it.value()
        item_total_position = 1 + len(self.coders)
        while item:
            line = ""
            for i in range(0, len(header)):
                line += "," + item.text(i)
            data += line[1:] + "\n"
            #self.depthgauge(item)
            it += 1
            item = it.value()
        f = open(filename, 'w')
        f.write(data)
        f.close()
        logger.info("Report exported to " + filename)
        mb = QtWidgets.QMessageBox()
        mb.setStyleSheet("* {font-size:" + str(self.app.settings['fontsize']) + "pt} ")
        mb.setWindowTitle(_('Csv file Export'))
        msg = filename + _(" exported")
        mb.setText(msg)
        mb.exec_()
        self.parent_textEdit.append(_("Coding frequencies csv file exported to: ") + filename)
        '''

    def closeEvent(self, event):
        """ Save dialog and splitter dimensions. """

        self.app.settings['dialogcodecrossovers_w'] = self.size().width()
        self.app.settings['dialogcodecrossovers_h'] = self.size().height()
        sizes = self.ui.splitter.sizes()
        self.app.settings['dialogcodecrossovers_splitter0'] = sizes[0]
        self.app.settings['dialogcodecrossovers_splitter1'] = sizes[1]
