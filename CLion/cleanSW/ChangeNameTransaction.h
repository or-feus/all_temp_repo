//
// Created by Feus on 2023/04/10.
//

#ifndef CLEANSW_CHANGENAMETRANSACTION_H
#define CLEANSW_CHANGENAMETRANSACTION_H
#include "ChangeEmployeeTransaction.h"
#include <string>

using namespace std;

class ChangeNameTransaction : public ChangeEmployeeTransaction {
public:
	virtual ~ChangeNameTransaction();
	ChangeNameTransaction(int empid, string name);
	virtual void Change(Employee&);

private:
	string itsName;
};


#endif //CLEANSW_CHANGENAMETRANSACTION_H
