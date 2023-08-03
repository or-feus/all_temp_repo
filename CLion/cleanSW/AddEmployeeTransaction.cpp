//
// Created by Feus on 2023/04/08.
//

#include "AddEmployeeTransaction.h"
#include "PayrollDatabase.h"

class PaymentSchedule;
class PaymentClassification;

extern PayrollDatabase GpayrollDatabase;

AddEmployeeTransaction::~AddEmployeeTransaction() {
}

AddEmployeeTransaction::AddEmployeeTransaction(
		int empId,
		std::string name,
		std::string address) :
		itsEmpId(empId),
		itsName(name),
		itsAddress(address){
}

void AddEmployeeTransaction::Execute() {
	PaymentClassification *pc = GetClassification();
	PaymentSchedule *ps = GetSchedule();
	PaymentMethod* pm = new HoldMethod();
	Employee *e = new Employee(itsEmpId, itsName, itsAddress);
	e->SetClassification(pc);
	e->SetSchedule(ps);
	e->SetMethod(pm);
	GpayrollDatabase.AddEmployee(itsEmpId, e);
}

