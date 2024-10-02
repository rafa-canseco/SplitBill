# Expense Sharing dApp Backend

## Overview

This backend supports a decentralized application (dApp) that allows users to track and balance expenses among multiple participants in shared events. It simplifies debt tracking and payment balancing by automating calculations and providing a clear overview of who owes what.

## Features

- Track expenses for multiple users across various sessions
- Automatically calculate and balance debts at checkout
- Simplify payment process without needing bank account details

## How It Works

### Example Scenario

#### Session: Thai Food
- Alice pays $100
- Bob pays $20

#### Session: Cinema
- Alice pays $20
- Bob pays $50

#### Total Expenses
- Total: $120 + $70 = $190
- Alice's total: $100 + $20 = $120
- Bob's total: $20 + $50 = $70

#### Rebalance Calculation
- Fair share per person: $190 / 2 = $95
- Alice's balance: $120 - $95 = +$25 (overpaid)
- Bob's balance: $70 - $95 = -$25 (underpaid)

#### Result
Bob sends $25 to the smart contract, which then sends $25 to Alice, resulting in a balanced state with all debts paid.

## Benefits

1. No need for manual calculations or expense tracking
2. Eliminates the need to exchange personal banking information
3. Streamlines the entire process of shared expense management

## Technical Stack

- Backend: Python with FastAPI
- Database: Supabase

