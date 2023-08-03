//
// Created by Feus on 2023/04/10.
//

#ifndef CLEANSW_CHANGECLASSIFICATIONTRANSACTION_H
#define CLEANSW_CHANGECLASSIFICATIONTRANSACTION_H
#include "ChangeEmployeeTransaction.h"

class PaymentClassification;
class PaymentSchedule;

class ChangeClassificationTransaction : public ChangeEmployeeTransaction{
public:
	virtual ~ChangeClassificationTransaction();
	ChangeClassificationTransaction(int empid);
	virtual void Change(Employee&);
	virtual PaymentClassification* GetClassification() const = 0;
	virtual PaymentSchedule* GetSchedule() const = 0;
};


#endif //CLEANSW_CHANGECLASSIFICATIONTRANSACTION_H
