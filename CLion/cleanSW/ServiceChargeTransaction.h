//
// Created by Feus on 2023/04/10.
//

#ifndef CLEANSW_SERVICECHARGETRANSACTION_H
#define CLEANSW_SERVICECHARGETRANSACTION_H
#include "Transaction.h"

class ServiceChargeTransaction : public Transaction {
public:
	virtual ~ServiceChargeTransaction();
	ServiceChargeTransaction(int memberId, long date, double charge);
	virtual void Execute();

private:
	int itsMemberid;
	long itsDate;
	double itsCharge;
};


#endif //CLEANSW_SERVICECHARGETRANSACTION_H
