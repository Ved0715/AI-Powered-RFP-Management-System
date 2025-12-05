import os
from typing import List, Dict
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()


def compare_proposals(rfp_data: Dist, proposals: List[Dict] ) -> Dict:

    proposals_text = ""
    for i, proposal in enumerate(proposals, 1):
        proposals_text += f"\n\n=== PROPOSAL {i} ===\n"
        proposals_text += f"Vendor ID: {proposal.get('vendor_id')}\n"
        proposals_text += f"Total Price: ${proposal.get('total_price'):,.2f}\n" if proposal.get('total_price') else "Total Price: Not specified\n"
        proposals_text += f"Delivery Time: {proposal.get('delivery_time')}\n" if proposal.get('delivery_time') else ""
        proposals_text += f"Payment Terms: {proposal.get('terms')}\n" if proposal.get('terms') else ""
        proposals_text += f"Warranty: {proposal.get('warranty')}\n" if proposal.get('warranty') else ""
        if proposal.get('line_items'):
            proposals_text += "Line Items:\n"
            for item in proposal.get('line_items', []):
                proposals_text += f"  - {item.get('item')}: ${item.get('price'):,.2f}\n" if item.get('price') else f"  - {item.get('item')}\n"

    rfp_text = f"""
RFP Requirements:
- Title: {rfp_data.get('title')}
- Description: {rfp_data.get('description')}
- Budget: ${rfp_data.get('budget'):,.2f}
- Deadline: {rfp_data.get('deadline')}
- Requirements: {', '.join(rfp_data.get('requirements', []))}
- Payment Terms: {rfp_data.get('payment_terms')}
- Warranty Terms: {rfp_data.get('warranty_terms')}
"""


    # defining agents
    cost_analyst = Agent(
        role='Cost Analyst',
        goal='Analyze pricing and value for money',
        backstory='Expert financial analyst specializing in procurement cost analysis and budget optimization.',
        verbose=False,
        allow_delegation=False
    )

    quality_assessor = Agent(
        role='Quality Assessor',
        goal='Evaluate product quality, warranty, and vendor reliability',
        backstory='Quality assurance specialist with 15 years of experience in vendor evaluation and product assessment.',
        verbose=False,
        allow_delegation=False
    )

    compliance_checker = Agent(
        role='Compliance Checker',
        goal='Verify if proposals meet RFP requirements',
        backstory='Compliance officer ensuring all vendor proposals align with specified requirements and regulations.',
        verbose=False,
        allow_delegation=False
    )

    decision_maker = Agent(
        role='Procurement Decision Maker',
        goal='Synthesize all analyses and recommend the best vendor',
        backstory='Senior procurement manager with expertise in vendor selection and strategic decision-making.',
        verbose=False,
        allow_delegation=True
    )

    #defining tasks

    #cost analysis task
    cost_analysis_task = Task(
        description=f"""
Analyze the cost-effectiveness of each proposal.

{rfp_text}

{proposals_text}

Provide:
1. Price comparison for each proposal
2. Value for money assessment
3. Budget compliance check
4. Cost ranking (1=best, 2=second, etc.)
""",
        agent=cost_analyst,
        expected_output="Cost analysis with rankings and budget assessment"
    )

    # quality assisment task
    quality_assessment_task = Task(
        description=f"""
Assess the quality aspects of each proposal.

{rfp_text}

{proposals_text}

Evaluate:
1. Warranty terms adequacy
2. Delivery timeline feasibility
3. Payment terms reasonableness
4. Overall quality indicators
5. Quality ranking (1=best, 2=second, etc.)
""",
        agent=quality_assessor,
        expected_output="Quality assessment with rankings"
    )

    #complience check task
    compliance_check_task = Task(
        description=f"""
Check compliance of each proposal with RFP requirements.

{rfp_text}

{proposals_text}

Verify:
1. All requirements are addressed
2. Specifications match
3. Terms align with RFP
4. Compliance score (0-100) for each proposal
""",
        agent=compliance_checker,
        expected_output="Compliance check with scores"
    )

    #final desition task
    final_decision_task = Task(
        description=f"""
Based on cost analysis, quality assessment, and compliance check, make a final recommendation.

Synthesize the findings and recommend:
1. Which vendor to select (Proposal 1, 2, 3, etc.)
2. Overall score for each proposal (0-100)
3. Top 3 reasons why the recommended vendor is best
4. Any risks or concerns
5. Summary comparison table

Format your response as:
RECOMMENDED VENDOR: Proposal X
OVERALL SCORES:
- Proposal 1: XX/100
- Proposal 2: XX/100
(for all proposals)

TOP REASONS:
1. [Reason]
2. [Reason]
3. [Reason]

RISKS/CONCERNS:
[List any concerns]

COMPARISON SUMMARY:
[Brief comparison table or summary]
""",
        agent=decision_maker,
        expected_output="Final recommendation with scores and reasoning",
        context=[cost_analysis_task, quality_assessment_task, compliance_check_task]
    )


    #creating crew
    crew = Crew(
        agents=[cost_analyst, quality_assessor, compliance_checker, decision_maker],
        tasks=[cost_analysis_task, quality_assessment_task, compliance_check_task, final_decision_task],
        process=Process.sequential,
        verbose=False
    )

    try:
        result = crew.kickoff()
        result_text = str(result)
        
        recommended = "Unknown"
        if "RECOMMENDED VENDOR:" in result_text:
            line = [l for l in result_text.split('\n') if 'RECOMMENDED VENDOR:' in l][0]
            recommended = line.split(':')[1].strip()
        
        scores = {}
        if "OVERALL SCORES:" in result_text:
            score_section = result_text.split("OVERALL SCORES:")[1].split("TOP REASONS:")[0]
            for line in score_section.strip().split('\n'):
                if 'Proposal' in line and '/' in line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        proposal_num = parts[0].strip()
                        score = parts[1].strip().split('/')[0].strip()
                        scores[proposal_num] = int(score) if score.isdigit() else 0
        
        #extract reasons
        reasons = []
        if "TOP REASONS:" in result_text:
            reasons_section = result_text.split("TOP REASONS:")[1].split("RISKS/CONCERNS:")[0]
            for line in reasons_section.strip().split('\n'):
                if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-')):
                    reasons.append(line.strip())
        
        return {
            "success": True,
            "recommended_vendor": recommended,
            "scores": scores,
            "reasons": reasons,
            "full_analysis": result_text,
            "summary": result_text.split("COMPARISON SUMMARY:")[1].strip() if "COMPARISON SUMMARY:" in result_text else ""
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "recommended_vendor": None,
            "scores": {},
            "reasons": [],
            "full_analysis": "",
            "summary": ""
        }



