//
// Created by Feus on 2023/04/10.
//

#include "ChangeEmployeeTransaction.h"
#include "PayrollDatabase.h"

extern PayrollDatabase GpayrollDatabase;

ChangeEmployeeTransaction:: ~ChangeEmployeeTransaction() {}

ChangeEmployeeTransaction::ChangeEmployeeTransaction(int empid)
	: itsEmpid(empid) {

}

void ChangeEmployeeTransaction::Execute() {
	Employee *e = GpayrollDatabase.GetEmployee(itsEmpid);
	if(e != 0) Change(*e);
}