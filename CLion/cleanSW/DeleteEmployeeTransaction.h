//
// Created by Feus on 2023/04/08.
//

#ifndef CLEANSW_DELETEEMPLOYEETRANSACTION_H
#define CLEANSW_DELETEEMPLOYEETRANSACTION_H
#include "Transaction.h"

class DeleteEmployeeTransaction {
public:
	virtual ~DeleteEmployeeTransaction();

	DeleteEmployeeTransaction(int empid);

	virtual void Execute();
private:
	int itsEmpid;
};


#endif //CLEANSW_DELETEEMPLOYEETRANSACTION_H
