from huggingface_hub import InferenceClient
def writeToFile(path, prompt):
    file = open(path, 'w')
    file.write(prompt)
    file.close()


if __name__ == "__main__":
    client = InferenceClient()
    system = """ "story" can be defined as a structured representation of information that outlines a specific theme or subject matter. each "story" consists set of attributes that provide detailed data points related to that theme. The attributes serve to describe various aspects of the story, allowing for a comprehensive understanding of the subject.   
    """
    first_response = client.text_generation(
        prompt=f"""
        {system}\n
        Generate a diverse set of story structures. Each structure should emphasize a unique organizational style, such as flat layouts, nested objects, lists, hierarchical data, and use of optional or conditional fields. Avoid focusing on the content theme itself; instead, vary the structure of the data. Aim to create structures with combinations of these elements to support different levels of complexity.

    For example, create structures like:

    A simple flat structure with a list of attributes.
    A nested structure where each main attribute has several sub-attributes.
    A hierarchical structure with parent-child relationships.
    A structure that includes optional fields or arrays of objects.
    A structure with relationships between fields, such as dependent values.
    Provide at least 10 different structures, with brief descriptions of each, focusing solely on the structure style.

    send only a description of each story structure""",
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.8,
        max_new_tokens=400,
        seed=54,
        return_full_text=False,
    )
    print(first_response)
