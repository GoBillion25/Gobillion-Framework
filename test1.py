import streamlit as st

def main():
    st.title("Fixed Container with Input at the Bottom")

    # Load external CSS file
    st.markdown(
        """
        <link rel="stylesheet" type="text/css" href="styles.css">
        """,
        unsafe_allow_html=True
    )

    # Content of the app
    st.write("Scrollable content goes here")

    # Default value for the input field
    default_input_value = "Default Value"

    # Fixed container with input at the bottom
    input_value = st.text_input("Enter something", value=default_input_value)

    st.markdown(
        """
        <div class="footer">
            <form>
                <label for="input_field">Input:</label><br>
                <input type="text" id="input_field" name="input_field" value="{0}"><br><br>
                <input type="submit" value="Submit">
            </form>
        </div>
        """.format(input_value),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
