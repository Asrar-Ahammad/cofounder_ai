"""Canonical gazette and statute corpus provider for legal RAG."""

from packages.rag.chunk_statute import chunk_statute_document
from packages.rag.index_store import StatuteIndexStore

_DPDP_TEXT = """
Section 4 Grounds for processing personal data
A person may process the personal data of a Data Principal only in accordance with the provisions of this Act and for a lawful purpose for which the Data Principal has given consent.

Section 6 Notice and consent
Every request for consent shall be accompanied or preceded by a notice given by the Data Fiduciary to the Data Principal informing her of the personal data to be processed and the purpose of processing.

Section 8 General obligations of Data Fiduciary
A Data Fiduciary shall implement appropriate technical and organisational measures to ensure effective adherence with the provisions of this Act and protect personal data against breach.
"""

_DGCL_TEXT = """
Section 101 Incorporators; how corporation formed; purposes
Any person, partnership, association or corporation, singly or jointly with others, may incorporate or organize a corporation under this chapter by filing a certificate of incorporation with the Division of Corporations in the Department of State.

Section 102 Contents of certificate of incorporation
The certificate of incorporation shall set forth the name of the corporation, the address of the corporation registered office in Delaware, the nature of the business or purposes to be conducted or promoted, and total authorized shares.
"""

_GDPR_TEXT = """
Article 5 Principles relating to processing of personal data
Personal data shall be processed lawfully, fairly and in a transparent manner in relation to the data subject and collected for specified, explicit and legitimate purposes.

Article 6 Lawfulness of processing
Processing shall be lawful only if and to the extent that at least one legal basis applies, including consent of the data subject, performance of a contract, or compliance with a legal obligation.
"""


def load_default_legal_index() -> StatuteIndexStore:
    """Build and populate a default StatuteIndexStore with standard venture statutes.

    Returns:
        StatuteIndexStore: Store loaded with India, Delaware, and EU corporate & data statutes.
    """
    store = StatuteIndexStore()
    dpdp_chunks = chunk_statute_document(
        act_name="Digital Personal Data Protection Act",
        jurisdiction="IN",
        raw_text=_DPDP_TEXT,
        source_url="https://www.meity.gov.in/writereaddata/files/Digital_Personal_Data_Protection_Act_2023.pdf",
        enacted_year=2023,
    )
    dgcl_chunks = chunk_statute_document(
        act_name="Delaware General Corporation Law",
        jurisdiction="US-DE",
        raw_text=_DGCL_TEXT,
        source_url="https://delcode.delaware.gov/title8/c001/sc01/",
        enacted_year=2020,
    )
    gdpr_chunks = chunk_statute_document(
        act_name="General Data Protection Regulation",
        jurisdiction="EU",
        raw_text=_GDPR_TEXT,
        source_url="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679",
        enacted_year=2016,
    )
    store.add_chunks(dpdp_chunks + dgcl_chunks + gdpr_chunks)
    return store
