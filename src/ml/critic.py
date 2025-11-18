"""Critical analysis and skepticism module."""

import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class CriticalAnalyzer:
    """Analyzes text for logical gaps, unsupported claims, and weaknesses."""

    # Patterns indicating unsupported claims
    CLAIM_PATTERNS = [
        r'will\s+(?:definitely|certainly|surely)\s+\w+',
        r'(?:always|never|all|every|none)\s+\w+',
        r'studies show(?!\s+\()',  # "studies show" without citation
        r'experts? (?:say|believe|think)(?!\s+\()',  # expert opinion without citation
        r'it is (?:proven|obvious|clear) that',
        r'\d+%(?!\s+\()',  # percentage without source
        r'everyone knows that',
        r'clearly\s+\w+',
        r'without (?:a )?doubt'
    ]

    # Logical fallacy indicators
    FALLACY_PATTERNS = {
        'Appeal to Authority': r'(?:famous|renowned|expert)\s+\w+\s+(?:says|believes)',
        'False Dichotomy': r'(?:either|only two)\s+(?:options?|choices?|ways?)',
        'Slippery Slope': r'if\s+\w+.*then\s+\w+.*and\s+then',
        'Correlation vs Causation': r'because\s+\w+.*therefore',
        'Hasty Generalization': r'(?:all|every|always)\s+\w+\s+(?:are|do|have)'
    }

    # Question words for generating follow-ups
    QUESTION_STARTERS = [
        "What are the potential limitations of",
        "How does this account for",
        "What evidence supports the claim that",
        "What alternative explanations exist for",
        "How would this apply to",
        "What are the ethical implications of",
        "Who might be negatively affected by"
    ]

    def identify_unsupported_claims(self, text: str) -> List[str]:
        """
        Identify potentially unsupported claims in text.

        Args:
            text: Input text to analyze

        Returns:
            List of identified unsupported claims
        """
        claims = []
        sentences = text.split('.')

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short sentences
                continue

            for pattern in self.CLAIM_PATTERNS:
                if re.search(pattern, sentence, re.IGNORECASE):
                    # Extract the claim (limit to 150 chars)
                    claim = sentence[:150] + '...' if len(sentence) > 150 else sentence
                    claims.append(claim)
                    break  # One claim per sentence

        return claims[:5]  # Return top 5

    def identify_logical_gaps(self, text: str) -> List[str]:
        """
        Identify potential logical fallacies and gaps.

        Args:
            text: Input text to analyze

        Returns:
            List of identified logical issues
        """
        gaps = []

        for fallacy_name, pattern in self.FALLACY_PATTERNS.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in list(matches)[:2]:  # Max 2 per fallacy type
                context_start = max(0, match.start() - 50)
                context_end = min(len(text), match.end() + 100)
                context = text[context_start:context_end].strip()
                gaps.append(f"Possible {fallacy_name}: '{context}...'")

        # Check for missing citations
        if 'research' in text.lower() or 'study' in text.lower():
            if not re.search(r'\(\d{4}\)|\[\d+\]', text):  # No year citations or references
                gaps.append("Research mentioned but no citations provided")

        # Check for vague quantifiers
        if re.search(r'many|some|few|several', text, re.IGNORECASE):
            gaps.append("Vague quantifiers used without specific data")

        return gaps[:5]  # Return top 5

    def generate_critical_summary(self, text: str, unsupported_claims: List[str],
                                   logical_gaps: List[str]) -> str:
        """
        Generate a critical analysis summary.

        Args:
            text: Original text
            unsupported_claims: List of unsupported claims
            logical_gaps: List of logical gaps

        Returns:
            Critical analysis summary
        """
        parts = []

        # Overall assessment
        if unsupported_claims or logical_gaps:
            parts.append("This article presents several claims that warrant scrutiny.")
        else:
            parts.append("This article appears well-reasoned with supported arguments.")

        # Mention unsupported claims
        if unsupported_claims:
            parts.append(
                f"There are {len(unsupported_claims)} potentially unsupported claims "
                "that would benefit from additional evidence or citations."
            )

        # Mention logical gaps
        if logical_gaps:
            parts.append(
                f"The analysis identified {len(logical_gaps)} potential logical issues "
                "or areas requiring more rigorous argumentation."
            )

        # Check for balance
        if 'however' not in text.lower() and 'although' not in text.lower():
            parts.append("The article may lack counterarguments or alternative perspectives.")

        # Check for sources
        citation_count = len(re.findall(r'\(\d{4}\)|\[\d+\]|et al\.', text))
        if citation_count == 0:
            parts.append("No academic citations were detected in the text.")
        elif citation_count < 3:
            parts.append("The article contains limited citations.")

        return ' '.join(parts)

    def generate_follow_up_questions(self, text: str, topics: List[str]) -> List[str]:
        """
        Generate thoughtful follow-up questions.

        Args:
            text: Input text
            topics: Main topics identified

        Returns:
            List of follow-up questions
        """
        questions = []

        # Extract key claims
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 30]

        # Generate questions based on claims
        if sentences:
            main_claim = sentences[0]
            questions.append(f"What evidence supports the assertion that {main_claim.lower()}?")

        # Topic-based questions
        if topics:
            questions.append(f"How does this relate to broader issues in {topics[0].lower()}?")
            if len(topics) > 1:
                questions.append(
                    f"What is the connection between {topics[0]} and {topics[1]} in this context?"
                )

        # Generic critical questions
        questions.extend([
            "What counterarguments or alternative viewpoints exist?",
            "What are the practical implications of implementing these ideas?",
            "What might critics of this perspective say?",
            "What further research would strengthen these conclusions?"
        ])

        return questions[:5]

    def suggest_related_topics(self, text: str, current_topics: List[str]) -> List[str]:
        """
        Suggest related topics for further reading.

        Args:
            text: Input text
            current_topics: Already identified topics

        Returns:
            List of related topic suggestions
        """
        related = []

        # Domain-specific relationships
        topic_map = {
            "Technology": ["Artificial Intelligence", "Cybersecurity", "Digital Privacy"],
            "Science": ["Research Methodology", "Scientific Ethics", "Peer Review"],
            "Healthcare": ["Medical Ethics", "Public Health Policy", "Healthcare Economics"],
            "Politics": ["Political Philosophy", "Governance", "Policy Analysis"],
            "Economics": ["Behavioral Economics", "Market Theory", "Economic Policy"],
            "Environment": ["Climate Science", "Sustainability", "Environmental Policy"],
            "Education": ["Pedagogy", "Educational Technology", "Learning Theory"]
        }

        for topic in current_topics:
            if topic in topic_map:
                related.extend(topic_map[topic])

        # Extract key terms from text
        words = text.lower().split()
        keyword_topics = {
            'ai': 'Machine Learning Applications',
            'data': 'Data Science and Analytics',
            'climate': 'Climate Change',
            'policy': 'Public Policy',
            'market': 'Market Economics',
            'social': 'Social Impact',
            'research': 'Research Methodology'
        }

        for keyword, topic_name in keyword_topics.items():
            if keyword in words and topic_name not in related:
                related.append(topic_name)

        return list(set(related))[:5]  # Return unique items, max 5

    def analyze(self, text: str, topics: List[str]) -> Dict:
        """
        Perform complete critical analysis.

        Args:
            text: Input text
            topics: Previously identified topics

        Returns:
            Dictionary with critical analysis results
        """
        logger.info("Performing critical analysis")

        unsupported_claims = self.identify_unsupported_claims(text)
        logical_gaps = self.identify_logical_gaps(text)

        return {
            'unsupported_claims': unsupported_claims,
            'logical_gaps': logical_gaps,
            'critical_summary': self.generate_critical_summary(
                text, unsupported_claims, logical_gaps
            ),
            'follow_up_questions': self.generate_follow_up_questions(text, topics),
            'related_topics': self.suggest_related_topics(text, topics)
        }
