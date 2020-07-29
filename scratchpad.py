# QGROUP: Readings
self.legend_box_refsig = Legend_box(
        text=["ref_X*", "ref_Y*", "sig_I"],
        pen=[self.PEN_01, self.PEN_02, self.PEN_03],
        checked=[False, False, True])
([chkb.clicked.connect(self.process_chkbs_legend_box_refsig) for chkb
  in self.legend_box_refsig.chkbs])
  
  
  
@QtCore.pyqtSlot()
def process_chkbs_legend_box_refsig(self):
    if self.lockin.lockin_paused:
        self.update_chart_refsig()      # Force update graph
  

  
@QtCore.pyqtSlot()
def update_chart_refsig(self):
    [CH.update_curve() for CH in self.CHs_refsig]
    for i in range(3):
        self.CHs_refsig[i].curve.setVisible(
                self.legend_box_refsig.chkbs[i].isChecked())