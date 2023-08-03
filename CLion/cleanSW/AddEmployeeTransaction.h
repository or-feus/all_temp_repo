//
// Created by Feus on 2023/04/08.
//

#ifndef CLEANSW_ADDEMPLOYEETRANSACTION_H
#define CLEANSW_ADDEMPLOYEETRANSACTION_H

#include "Transaction.h"
#include <string>

using namespace std;

class PaymentClassification;

class PaymentSchedule;

class AddEmployeeTransaction : public Transaction {
public:
	virtual ~AddEmployeeTransaction();

	AddEmployeeTransaction(int empId, string name, string address);
	virtual PaymentClassification* GetClassification() const = 0;
	virtual PaymentSchedule* GetSchedule() const = 0;
	virtual void Execute();

private:
	int itsEmpId;
	string itsName;
	string itsAddress;
};


#endif //CLEANSW_ADDEMPLOYEETRANSACTION_H
