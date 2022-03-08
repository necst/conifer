# Entree: the first automatic design flow for deploying the inference of large Decision Tree (DT) ensembles on FPGA-enabled embedded devices

Entree generates hardware accelerators for arbitrarily large DT ensembles on embedded-class heterogeneous Systems-on-a-Chip (SoCs) mounting an FPGA.

Its design flow automatically instantiates a template hardware architecture that exploits the FPGA’s partial dynamic reconfiguration capabilities to host an arbitrarily numerous DT ensemble on it.

## Acknowledging

If you wish to contribute, extend, or exploit as-is the Entree project, you are required to cite our paper:

>A. Damiani, E. Del Sozzo, and M. D. Santambrogio, “Large Forests and Where to ‘Partially’ Fit Them”, in Proceedings of the 27th Asia and South Pacific Design Automation Conference, 2022 (Accepted to appear).

```BibTeX
@INPROCEEDINGS{9712534,
  author={Damiani, Andrea and Sozzo, Emanuele Del and Santambrogio, Marco D.},
  booktitle={2022 27th Asia and South Pacific Design Automation Conference (ASP-DAC)}, 
  title={Large Forests and Where to “Partially” Fit Them}, 
  year={2022},
  volume={},
  number={},
  pages={550-555},
  doi={10.1109/ASP-DAC52403.2022.9712534}}
```

## Acknowledgments

Based on the High-Level Synthesis Decision Tree implementation of the [https://github.com/thesps/conifer](conifer) project, it inherits the translation of models from `sklearn`, `xgboost`, and `TMVA`.

>S. Summers et al., "Fast inference of Boosted Decision Trees in FPGAs for particle physics", Journal of Instrumentation, vol. 15, no. 05, pp. P05026-P05026, 2020. Available: 10.1088/1748-0221/15/05/p05026.

```BibTeX
@article{summers2020fast,
  title={Fast inference of boosted decision trees in FPGAs for particle physics},
  author={Summers, Sioni and Di Guglielmo, Giuseppe and Duarte, Javier and Harris, Philip and Hoang, Duc and Jindariani, Sergo and Kreinar, Edward and Loncar, Vladimir and Ngadiuba, Jennifer and Pierini, Maurizio and others},
  journal={Journal of Instrumentation},
  volume={15},
  number={05},
  pages={P05026},
  year={2020},
  publisher={IOP Publishing}
}
```
