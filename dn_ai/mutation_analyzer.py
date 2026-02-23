"""
Mutation Analysis - Identify and analyze DNA mutations
"""

import pandas as pd
import numpy as np
from collections import Counter

class MutationAnalyzer:
    """Analyze mutations in DNA sequences"""
    
    @staticmethod
    def identify_mutations(sequence1: str, sequence2: str) -> list:
        """
        Identify differences between two sequences
        
        Args:
            sequence1: Reference sequence
            sequence2: Sequence to compare
            
        Returns:
            List of mutations with positions and changes
        """
        mutations = []
        for i, (base1, base2) in enumerate(zip(sequence1, sequence2)):
            if base1 != base2:
                mutations.append({
                    'position': i,
                    'reference': base1,
                    'mutant': base2,
                    'mutation': f"{base1}{i}{base2}"
                })
        return mutations
    
    @staticmethod
    def analyze_mutation_types(df: pd.DataFrame) -> dict:
        """
        Analyze types of mutations in the dataset
        
        Args:
            df: DataFrame with sequences and mutation flags
            
        Returns:
            Dictionary with mutation statistics
        """
        mutant_sequences = df[df['Mutation_Flag'] == 1]
        wildtype_sequences = df[df['Mutation_Flag'] == 0]
        
        stats = {
            'total_sequences': len(df),
            'mutant_count': len(mutant_sequences),
            'wildtype_count': len(wildtype_sequences),
            'mutation_percentage': (len(mutant_sequences) / len(df) * 100),
            'mutant_by_class': mutant_sequences['Class_Label'].value_counts().to_dict(),
            'wildtype_by_class': wildtype_sequences['Class_Label'].value_counts().to_dict(),
        }
        
        return stats
    
    @staticmethod
    def get_mutant_sequences(df: pd.DataFrame, limit: int = 20) -> pd.DataFrame:
        """Get sequences with mutations"""
        mutants = df[df['Mutation_Flag'] == 1][['Sample_ID', 'Sequence', 'Class_Label', 'Disease_Risk']].head(limit)
        return mutants
    
    @staticmethod
    def get_wildtype_sequences(df: pd.DataFrame, limit: int = 20) -> pd.DataFrame:
        """Get wild-type sequences"""
        wildtype = df[df['Mutation_Flag'] == 0][['Sample_ID', 'Sequence', 'Class_Label', 'Disease_Risk']].head(limit)
        return wildtype
    
    @staticmethod
    def analyze_nucleotide_changes(df: pd.DataFrame) -> dict:
        """Analyze which nucleotides change most frequently"""
        mutant_df = df[df['Mutation_Flag'] == 1]
        wildtype_df = df[df['Mutation_Flag'] == 0]
        
        changes = Counter()
        
        for mut_seq, wt_seq in zip(mutant_df['Sequence'].values, 
                                    wildtype_df['Sequence'].sample(n=min(len(mutant_df), len(wildtype_df)), 
                                                                   random_state=42)['Sequence'].values):
            for m, w in zip(mut_seq, wt_seq):
                if m != w:
                    changes[f"{w}→{m}"] += 1
        
        return dict(changes.most_common(10))
    
    @staticmethod
    def generate_mutation_report(df: pd.DataFrame) -> str:
        """Generate comprehensive mutation analysis report"""
        analyzer = MutationAnalyzer()
        stats = analyzer.analyze_mutation_types(df)
        
        report = f"""
╔════════════════════════════════════════════════════════╗
║        DNA MUTATION ANALYSIS REPORT                    ║
╚════════════════════════════════════════════════════════╝

📊 DATASET STATISTICS
├─ Total Sequences: {stats['total_sequences']}
├─ Mutant Sequences: {stats['mutant_count']} ({stats['mutation_percentage']:.1f}%)
└─ Wild-type Sequences: {stats['wildtype_count']} ({100-stats['mutation_percentage']:.1f}%)

🧬 MUTATIONS BY CLASS
"""
        
        report += "\nMutant Distribution:\n"
        for cls, count in stats['mutant_by_class'].items():
            report += f"  • {cls}: {count}\n"
        
        report += "\nWild-type Distribution:\n"
        for cls, count in stats['wildtype_by_class'].items():
            report += f"  • {cls}: {count}\n"
        
        report += "\n" + "═" * 55
        
        return report


def main():
    """Main function"""
    # Load dataset
    df = pd.read_csv('synthetic_dna_dataset.csv')
    
    # Create analyzer
    analyzer = MutationAnalyzer()
    
    # Generate report
    report = analyzer.generate_mutation_report(df)
    print(report)
    
    # Display mutation statistics
    print("\n\n🔬 MUTANT SEQUENCES (First 5):")
    print("=" * 80)
    mutants = analyzer.get_mutant_sequences(df, limit=5)
    for idx, row in mutants.iterrows():
        print(f"\n{row['Sample_ID']} | Class: {row['Class_Label']} | Risk: {row['Disease_Risk']}")
        print(f"Sequence: {row['Sequence']}")
    
    print("\n\n🔬 WILD-TYPE SEQUENCES (First 5):")
    print("=" * 80)
    wildtype = analyzer.get_wildtype_sequences(df, limit=5)
    for idx, row in wildtype.iterrows():
        print(f"\n{row['Sample_ID']} | Class: {row['Class_Label']} | Risk: {row['Disease_Risk']}")
        print(f"Sequence: {row['Sequence']}")


if __name__ == "__main__":
    main()
