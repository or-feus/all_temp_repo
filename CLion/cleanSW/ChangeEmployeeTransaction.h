//
// Created by Feus on 2023/04/10.
//

#ifndef CLEANSW_CHANGEEMPLOYEETRANSACTION_H
#define CLEANSW_CHANGEEMPLOYEETRANSACTION_H
#include "Transaction.h"

class ChangeEmployeeTransaction : public Transaction {
public:
	ChangeEmployeeTransaction(int empid);
	virtual ~ChangeEmployeeTransaction();
	virtual void Execute();
	virtual void Change(Employee&) = 0;

private:
	int itsEmpid;
};


#endif //CLEANSW_CHANGEEMPLOYEETRANSACTION_H
