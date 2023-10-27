import sys
from pyteal import *

VOTING_CREDIT_SYM = Bytes("QVoteDecisionCredits")
OPTION_PREFIX = Bytes("option_")
NULL_OPTION = Bytes("NULL_OPTION")
ZERO = Int(2**32)
MINUS = Bytes("-")

def approval_program():
  arg_num = Txn.application_args.length()
  on_closeout = Return(Int(1))

  asset_id = App.globalGet(Bytes("asset_id"))
  asset_balance = AssetHolding.balance(Int(0), asset_id)
  asset_coeff = App.globalGet(Bytes("asset_coefficient"))

  on_option = Seq([
      If(Global.latest_timestamp() > App.globalGet(Bytes("voting_start_time")),
         Return(Int(0))),
      asset_balance,
      If(asset_balance.hasValue(),
          Seq([App.localPut(Int(0), VOTING_CREDIT_SYM, Mul(asset_balance.value(), asset_coeff)), Return(Int(1))]),
              Return(Int(0)))
  ])

  # TODO registration time 

  def on_add_options():
    if Global.latest_timestamp() > App.globalGet(Bytes("voting_start_time")):
        return Return(Int(0))
    for i in range(1, 6):
        if Txn.application_args[i] != NULL_OPTION:
            App.globalPut(Concat(OPTION_PREFIX, Txn.application_args[i]), ZERO)
    return Return(Int(1))

  def on_fund():
    if Global.latest_timestamp() < App.globalGet(Bytes("funding_start_time")) or Global.latest_timestamp() > App.globalGet(Bytes("funding_end_time")):
        return Return(Int(0))

    funding_pool = App.globalGet(Int(0), Bytes("funding_pool"))
    projects = App.globalGet(Int(0), Bytes("projects"))

    project_funding = quadratic_funding_formula(funding_pool, funding_coefficient, projects)

    for project in projects:
        App.globalPut(Int(0), project, project_funding[project])

    return Return(Int(1))

  def quadratic_funding_formula(funding_pool, funding_coefficient, projects):
    project_contributions = {}
    for project in projects:
        project_contributions[project] = 0
        for contribution in contributions:
            if contribution.project_id == project:
                project_contributions[project] += 1

    project_funding = {}
    for project in projects:
        project_funding[project] = funding_coefficient * project_contributions[project] ** 2

    total_funding = sum(project_funding.values())
    if total_funding > funding_pool:
        for project in projects:
            project_funding[project] = project_funding[project] / total_funding * funding_pool

    return project_funding

  on_creation = Seq([
      App.globalPut(Bytes("Creator"), Txn.sender()),
      App.globalPut(Bytes("Name"), Txn.application_args[0]),
      App.globalPut(Bytes("asset_id"), Btoi(Txn.application_args[6])),
      App.globalPut(Bytes("asset_coefficient"), Btoi(Txn.application_args[7])),
      App.globalPut(Bytes("voting_start_time"), Btoi(Txn.application_args[8])),
      App.globalPut(Bytes("voting_end_time"), Btoi(Txn.application_args[9])),
      on_add_options(),
      # Initialize funding
      App.globalPut(Int(0), Bytes("funding_pool"), funding_amount),
      # initial funding coefficient
      App.globalPut(Bytes("funding_coefficient"), funding_coefficient),
      Return(Int(1))
  ])

program = Cond(   
      [Txn.application_id() == Int(0), on_creation],   
      [Txn.on_completion() == OnComplete.DeleteApplication, Return(Int(0))], 
      [Txn.on_completion() == OnComplete.UpdateApplication, Return(Int(0))],   
      [Txn.on_completion() == OnComplete.OptIn, on_optin],
      [Txn.application_args[0] == Bytes("add_options"), on_add_options],
      [Txn.application_args[0] == Bytes("fund"), on_fund]
  )   

