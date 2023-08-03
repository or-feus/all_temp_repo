//
// Created by Feus on 2023/04/10.
//

#include "ChangeNameTransaction.h"

ChangeNameTransaction::~ChangeNameTransaction() {}

ChangeNameTransaction::ChangeNameTransaction(int empid, std::string name)
	: itsName(name){

}

void ChangeNameTransaction::Change(Employee& e){
	e.SetName(itsName);
}