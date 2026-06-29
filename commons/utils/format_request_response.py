def format_request_response(message: str) -> list[str]:
    final_tab: list[str] = []
    word_count = 0
    string = ""
    content_started = False
    for i in range(len(message)):
        if (word_count == 2 and message[i] != " ") or content_started:
            content_started = True
            string += message[i]
        else:
            if message[i] != " ":
                string += message[i]
            elif string != "":
                final_tab.append(string)
                word_count += 1
                string = ""
    if string != "":
        final_tab.append(string)
    return final_tab
