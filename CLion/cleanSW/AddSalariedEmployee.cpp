//
// Created by Feus on 2023/04/08.
//

#include "AddSalariedEmployee.h"


AddSalariedEmployee:: ~AddSalariedEmployee() {

}

AddSalariedEmployee::AddSalariedEmployee(
		int empid,
		std::string name,
		std::string address,
		double salary): AddEmployeeTransaction(
		empid,
		name,
		address),
		itsSalary(salary){

}

PaymentClassification* AddSalariedEmployee::GetClassification() const {
	return new SalariedClassification(itsSalary);
}

PaymentSchedule* AddSalariedEmployee::GetSchedule() const {
	return new MonthSchedule();
}