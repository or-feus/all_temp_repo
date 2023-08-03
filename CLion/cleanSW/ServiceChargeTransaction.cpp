//
// Created by Feus on 2023/04/10.
//

#include "ServiceChargeTransaction.h"
#include "PayrollDatabase.h"

extern PayrollDatabase GpayrollDatabase;

ServiceChargeTransaction::~ServiceChargeTransaction(){

}

ServiceChargeTransaction::ServiceChargeTransaction(int memberId, long date, double charge)
	: itsMemberid(memberId), itsDate(date), itsCharge(charge){

}

void ServiceChargeTransaction::Execute() {
	Employee *e = GpayrollDatabase.GetUnionMember(itsMemberid);
	Affilication* af = e -> GetAffilication();
	if(UnionAffilication* uaf = dynamic_cast<UnionAffiliation*>(af)){
		uaf->AddServiceCharge(itsDate, itsCharge);
	}
}