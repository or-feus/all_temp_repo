//
// Created by Feus on 2023/04/10.
//

#ifndef CLEANSW_CHANGEHOURLYTRANSACTION_H
#define CLEANSW_CHANGEHOURLYTRANSACTION_H
#include "ChangeClassificationTransaction.h"

class ChangeHourlyTransaction : public ChangeClassificationTransaction{
public:
	virtual ~ChangeHourlyTransaction();
	ChangeHourlyTransaction(int empid, double hourlyRate);
	virtual PaymentSchedule* GetSchedule() const;
	virtual PaymentClassification* GetClassification() const;

private:
	double itsHourlyRate;
};


#endif //CLEANSW_CHANGEHOURLYTRANSACTION_H
