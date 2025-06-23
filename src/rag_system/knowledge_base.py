"""
Insurance Knowledge Base for RAG System
"""

INSURANCE_KNOWLEDGE = [
    {
        "question": "What is covered under a standard homeowners policy for water damage?",
        "answer": """
        Standard homeowners policies (HO-3) typically cover water damage that is sudden and accidental from internal sources, such as:
        - Burst pipes
        - Accidental overflow from appliances (washing machines, dishwashers)
        - Leaking roof (damage to interior, not the roof itself)
        - Water damage from extinguishing a fire
        
        They typically DO NOT cover:
        - Flooding from external sources (requires separate flood insurance)
        - Sewer backup (unless endorsement is purchased)
        - Gradual leaks that occurred over weeks/months
        - Mold (may have limited coverage if resulting from covered water damage)
        - Water damage due to neglect or lack of maintenance
        
        Coverage is subject to the policy deductible, typically $1,000-$2,500.
        """
    },
    {
        "question": "What documentation is required for a water damage claim?",
        "answer": """
        For water damage claims, the following documentation is typically required:
        
        1. Detailed description of the damage (how, when, where it occurred)
        2. Photos/videos of the damage before repairs
        3. Inventory of damaged personal property
        4. Repair estimates from licensed contractors
        5. Receipts for emergency repairs or mitigation services
        6. Receipts or proof of ownership for damaged valuable items
        
        The insurance company may also send an adjuster to inspect the damage in person.
        """
    },
    {
        "question": "What are common signs of insurance fraud in water damage claims?",
        "answer": """
        Common indicators of potential fraud in water damage claims include:
        
        1. Multiple claims for the same property in a short period
        2. Claim filed shortly after policy inception or coverage increase
        3. Reluctance to provide documentation or access for inspection
        4. Documentation from contractors with inconsistent information
        5. Damage that appears inconsistent with the reported cause
        6. Excessive or unrelated items included in claim
        7. Contractor and policyholder appear to have a pre-existing relationship
        
        Insurance companies use special investigation units (SIU) to review suspicious claims.
        Fraudulent claims constitute 5-10% of all claims and cost the industry billions annually.
        """
    },
    {
        "question": "What is the process for handling a water damage claim?",
        "answer": """
        The standard process for handling water damage claims includes:
        
        1. Initial Notification (FNOL) - Customer reports the claim
        2. Assignment - Claim assigned to appropriate adjuster
        3. Coverage Verification - Confirm policy covers the type of water damage
        4. Damage Assessment - Adjuster inspects damage (in person or virtually)
        5. Mitigation Review - Ensure proper water extraction and drying occurred
        6. Estimate Creation - Detailed repair estimate prepared
        7. Settlement Offer - Payment amount determined based on policy terms
        8. Claim Resolution - Payment issued or repairs authorized
        
        Timeline varies but typically takes 2-4 weeks for straightforward claims.
        Complex claims may take longer, especially if extensive damage or coverage questions exist.
        """
    },
    {
        "question": "What is subrogation in insurance claims?",
        "answer": """
        Subrogation is the legal process where an insurance company, after paying a claim to its policyholder, seeks reimbursement from a third party who may be legally responsible for the loss.
        
        For example, in water damage claims:
        - If a washing machine hose fails due to a manufacturing defect, the insurer may subrogate against the manufacturer
        - If a neighbor's plumbing issue caused water damage to your property, your insurer may seek recovery from their insurance
        
        The process typically involves:
        1. Identifying potential third-party liability
        2. Gathering evidence of negligence or responsibility
        3. Sending demand letters to responsible parties
        4. Negotiating recovery amounts
        5. Litigation if necessary
        
        Successful subrogation helps insurers recover costs, which can help control premium increases.
        """
    },
    {
        "question": "What is actual cash value vs. replacement cost in insurance?",
        "answer": """
        These are two different methods insurers use to value property in claims:
        
        Actual Cash Value (ACV):
        - Replacement cost MINUS depreciation
        - Takes into account the item's age and condition
        - Results in lower claim payments
        - Example: A 10-year-old carpet damaged by water might be valued at 20% of its replacement cost
        
        Replacement Cost Value (RCV):
        - Cost to replace the item with a new, similar item at current market prices
        - Does not deduct for depreciation
        - Results in higher claim payments
        - Often paid in two steps: ACV first, then remaining amount after replacement
        
        Most standard homeowners policies cover personal property at ACV by default, with RCV available as an endorsement for additional premium.
        """
    }
]