import re

def chunk_markdown(content: str, source: str) -> list[dict]:
    chunks = []
    
    # Simple chunking by heading for rag_system_prompt.md
    if "rag_system_prompt" in source:
        sections = re.split(r'\n##\s+', content)
        for i, section in enumerate(sections):
            if not section.strip():
                continue
            title = section.split('\n')[0][:50]
            if i > 0:
                section = "## " + section
            chunks.append({
                "text": section.strip(),
                "metadata": {"source": source, "section": title}
            })
            
    # Simple chunking by separator for knowledge_base.md
    elif "knowledge_base" in source:
        sections = content.split("================================================================================")
        for section in sections:
            if not section.strip():
                continue
            url_match = re.search(r'URL: (.*)', section)
            url = url_match.group(1) if url_match else "unknown"
            chunks.append({
                "text": section.strip(),
                "metadata": {"source": source, "url": url}
            })
    else:
        # Semantic chunking by headers for structured data reports
        sections = re.split(r'\n(?=##\s+)', '\n' + content.strip())
        for i, section in enumerate(sections):
            if not section.strip():
                continue
            
            lines = section.strip().split('\n')
            title = lines[0].replace('## ', '').strip()[:50] if lines[0].startswith('## ') else f"Section {i}"
            
            if len(section) > 3000:
                sub_chunks = [section[j:j+3000] for j in range(0, len(section), 3000)]
                for j, sub_chunk in enumerate(sub_chunks):
                    chunks.append({
                        "text": sub_chunk.strip(),
                        "metadata": {"source": source, "section": f"{title} (part {j+1})"}
                    })
            else:
                chunks.append({
                    "text": section.strip(),
                    "metadata": {"source": source, "section": title}
                })
        
    return chunks
