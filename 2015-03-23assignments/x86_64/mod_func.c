#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _Cad_reg(void);
extern void _HH_traub_reg(void);
extern void _it2_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," Cad.mod");
    fprintf(stderr," HH_traub.mod");
    fprintf(stderr," it2.mod");
    fprintf(stderr, "\n");
  }
  _Cad_reg();
  _HH_traub_reg();
  _it2_reg();
}
