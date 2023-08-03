//
// Created by Feus on 2023/04/08.
//

#ifndef CLEANSW_ADDSALARIEDEMPLOYEE_H
#define CLEANSW_ADDSALARIEDEMPLOYEE_H
#include "AddEmployeeTransaction.h"

class AddSalariedEmployee : public AddEmployeeTransaction{
public:
	virtual ~AddSalariedEmployee();

	AddSalariedEmployee(int empid, string name, string address, double salary);
	PaymentClassification* GetClassification() const;
	PaymentSchedule* GetSchedule() const;

private:
	double itsSalary;
};


#endif //CLEANSW_ADDSALARIEDEMPLOYEE_H
