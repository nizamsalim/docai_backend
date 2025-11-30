class PromptBuilder:
    def get_initial_generation_prompt(
        self, project_title: str, project_type: str, section_title: str
    ):
        format_prompt = ""
        if project_type == "docx":
            format_prompt = (
                "The content should be detailed as seen in a report/document."
            )
        elif project_type == "pptx":
            format_prompt = (
                "The content should be concise and brief as seen in a presentation."
            )

        return f"""
            You are an AI assistant helping to create a new document of type {project_type}.
            {format_prompt}
            Return markdown content with appropriate formating, spacing, etc.
            Document title: {project_title}
            Write a high-quality first draft for a section titled: {section_title}
            The length should be not too long, nor too short. It should have moderate length.
            The tone should be clear, structured, and informative.
            Avoid filler sentences. Provide useful content. Include section title as heading in each section content
            Return only the requested text without any extra content.
        """

    def get_initial_sections_generation_prompt(
        self, project_title: str, project_type: str
    ):
        return f"""
            You are an AI assistant helping to create a new document of type {project_type}
            Document title: {project_title}
            Return 5 appropriate {"section titles" if project_type == "docx" else "slide titles"} related to the project title.
            Return the titles as a json array. Ensure that the titles align with the main document title and the returning formatting is followed strictly.
        """

    def get_refinement_prompt(
        self, section_title: str, existing_content: str, user_prompt: str, ctx=""
    ):
        context = f"Full document context:\n{ctx}" if ctx != "" else ""
        return f"""
            You are refining the content for a document
            Section title: {section_title}
            Existing content:\n{existing_content}
            User instructions:\n"{user_prompt}"
            \n\n
            {context}

            Rewrite the content according to the instruction while keeping meaning and formatting consistent.
            Ensure the output is final, clean, and ready to insert. Return only the requested text without any extra content
        """
