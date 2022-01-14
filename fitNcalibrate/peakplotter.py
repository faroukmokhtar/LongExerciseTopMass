#!/usr/bin/env python
import ROOT
from ROOT import *
from array import array
import tdrstyle

# Add a zero to the theoretical values to make a nice y=x plot
theor=array('d',[0.0,65.7403367994,67.570939637681,69.390239814814])
#exper=array('d',[64.3,66.05,66.97]) # Pseudo
exper=array('d',[64.56,65.4,66.52])
theor_err=array('d',[0.0079,0.0077,0.0076])
#exper_err=array('d',[0.14,0.14,0.135]) # Pseudo
exper_err=array('d',[0.2591,0.2538,0.2467])

#for i in range(0,len(exper)):
#    exper[i]=(exper[i]-16.51)/0.729
#    exper_err[i]=(exper_err[i])/0.729

c1 = TCanvas("canvas 1", "c1", 800, 600)
c1.cd()
tdrstyle.setTDRStyle()

graph = TGraphErrors(len(exper),theor[1:],exper,theor_err,exper_err)
graph.SetMarkerColor(4)
graph.SetMarkerStyle(21)
graph.SetTitle("")
graph.GetXaxis().SetTitleSize(0.04)
graph.GetXaxis().SetTitle("Predicted Energy Peak Position [GeV]")
graph.GetXaxis().SetTitleOffset(1.2)
graph.GetYaxis().SetTitleSize(0.04)
graph.GetYaxis().SetTitle("Measured Energy Peak Position [GeV]")
graph.GetYaxis().SetTitleOffset(1.3)

graph.GetXaxis().SetLimits(63,70)
graph.SetMaximum(67.5)
graph.SetMinimum(63)



gfit = TF1("f","[0] + [1] * x")
graph.Fit(gfit)

Covariance1 = TVirtualFitter.GetFitter().GetCovarianceMatrixElement(0,1)
print Covariance1
Covariance2 = TVirtualFitter.GetFitter().GetCovarianceMatrixElement(1,0)
print Covariance2
Variance0 = TVirtualFitter.GetFitter().GetCovarianceMatrixElement(0,0)
print Variance0
Variance1 = TVirtualFitter.GetFitter().GetCovarianceMatrixElement(1,1)
print Variance1

graph.Draw("AP")

ideal = TGraph(len(theor),theor,theor)
ideal.SetLineColor(4)
ideal.SetLineStyle(7)
ideal.Draw("SAME")

label1 = TLatex()
label1.SetNDC()
label1.SetTextFont(60)
label1.SetTextSize(0.07)
label1.SetTextAlign(31)
label1.DrawLatex(0.32, 0.92, "CMS DAS")
label2 = TLatex()
label2.SetNDC()
label2.SetTextFont(42)
label2.SetTextSize(0.06)
label2.SetTextAlign(11)
label2.DrawLatex(0.33, 0.92, "#it{Simulation}")

leg = TLegend(0.13,0.75,0.41,0.87)
leg.AddEntry(graph,"Simulation","p")
leg.AddEntry(ideal,"Expectation","l")
leg.AddEntry(gfit,"Fit","l")
leg.Draw("SAME")

gPad.Update()
stats = gPad.GetPrimitive("stats")
stats.__class__ = ROOT.TPaveStats
stats.SetY1NDC(0.1)
stats.SetY2NDC(0.4)
stats.SetX1NDC(0.6)
stats.SetX2NDC(0.9)

#a=input("")

# Save the plot
#gPad.RedrawAxis()
c1.SaveAs("calibration.png")


