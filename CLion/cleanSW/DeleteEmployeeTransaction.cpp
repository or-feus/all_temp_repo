//
// Created by Feus on 2023/04/08.
//

#include "DeleteEmployeeTransaction.h"
#include "PayrollDatabase.h"

extern PayrollDatabase GpayrollDatabase;

DeleteEmployeeTransaction::~DeleteEmployeeTransaction() {

}

DeleteEmployeeTransaction::DeleteEmployeeTransaction(int empid) : itsEmpid(empid){

}

void DeleteEmployeeTransaction::Execute() {
	GpayrollDatabase.DeleteEmployee(itsEmpid);
}