//
// Created by Feus on 2023/04/08.
//

#include "PayrollDatabase.h"

PayrollDatabase GpayrollDatabase;

PayrollDatabase:: ~PayrollDatabase() {
}

Employee* PayrollDatabase::GetEmployee(int empId) {
	return itsEmployees[empId];
}

void PayrollDatabase::AddEmployee(int empId, Employee* e) {
	itsEmployees[empId] = e;
}