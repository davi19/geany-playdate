/*
 *      errors.c - parse pdc output into Geany's Compiler tab
 *
 *      Matches the midouest vscode-playdate-debug problem matchers:
 *        warning: FILE:LINE: MESSAGE
 *        error:   FILE:LINE: MESSAGE
 *        error:   MESSAGE
 */

#include "playdate.h"

#include <string.h>

/* Number of compiler messages added in the current build (for summary). */
static guint msg_count = 0;
static guint warn_count = 0;
static guint error_count = 0;


void pd_errors_begin(void)
{
	msg_count = 0;
	warn_count = 0;
	error_count = 0;

	msgwin_clear_tab(MSG_COMPILER);
	msgwin_switch_tab(MSG_COMPILER, TRUE);
}


/* Emit in Geany's clickable form: path:line: severity: message */
static void emit(const gchar *severity, const gchar *file, gint line, const gchar *message)
{
	gint color = COLOR_BLACK;

	if (g_strcmp0(severity, "error") == 0)
	{
		color = COLOR_RED;
		error_count++;
	}
	else if (g_strcmp0(severity, "warning") == 0)
	{
		color = COLOR_DARK_RED;
		warn_count++;
	}
	msg_count++;

	if (line > 0 && !EMPTY(file))
		msgwin_compiler_add(color, "%s:%d: %s: %s", file, line, severity, message);
	else if (!EMPTY(file))
		msgwin_compiler_add(color, "%s: %s: %s", file, severity, message);
	else
		msgwin_compiler_add(color, "%s: %s", severity, message);
}


/*
 * Parse one line of pdc stdout/stderr.
 * Patterns (from midouest/vscode-playdate-debug):
 *   ^(warning|error):\s+(.*):(\d+):\s+(.*)$
 *   ^(error):\s+(.*)$
 * Also accept already-Geany-formatted "file:line: msg" passthrough.
 */
void pd_errors_parse_line(const gchar *line)
{
	gchar *work;
	gchar *p;
	const gchar *severity = NULL;

	if (line == NULL)
		return;

	work = g_strdup(line);
	g_strchomp(work);
	p = work;

	/* strip leading whitespace */
	while (*p == ' ' || *p == '\t')
		p++;

	if (*p == '\0')
	{
		g_free(work);
		return;
	}

	/* severity: rest */
	if (g_str_has_prefix(p, "warning:"))
	{
		severity = "warning";
		p += 8;
	}
	else if (g_str_has_prefix(p, "error:"))
	{
		severity = "error";
		p += 6;
	}
	else if (g_str_has_prefix(p, "Error:") || g_str_has_prefix(p, "ERROR:"))
	{
		severity = "error";
		p += 6;
	}

	while (*p == ' ' || *p == '\t')
		p++;

	if (severity != NULL)
	{
		/* Try FILE:LINE: MESSAGE */
		gchar *last_colon = strrchr(p, ':');
		gchar *first_colon = strchr(p, ':');

		/* Find the colon before the line number: prefer the pattern path:NNN: msg */
		if (first_colon != NULL)
		{
			gchar *rest;
			gchar *end = NULL;
			gint line_no;
			gboolean ok = FALSE;

			/* Scan for a ":<digits>: " or ":<digits>:" pattern.
			 * Use the last colon before a numeric field as the line separator. */
			{
				gchar *c = p;
				while ((c = strchr(c, ':')) != NULL)
				{
					gchar *num_start = c + 1;
					gchar *num_end = NULL;
					gint n = (gint) g_ascii_strtoll(num_start, &num_end, 10);

					if (num_end > num_start && (*num_end == ':' || *num_end == ' ' || *num_end == '\0'))
					{
						/* likely path:line */
						line_no = n;
						rest = num_end;
						if (*rest == ':')
							rest++;
						while (*rest == ' ' || *rest == '\t')
							rest++;

						{
							gchar *file = g_strndup(p, (gsize) (c - p));
							emit(severity, file, line_no, rest);
							g_free(file);
							ok = TRUE;
						}
						break;
					}
					c++;
				}
			}

			/* fallback: no line number found */
			if (!ok)
				emit(severity, NULL, 0, p);

			(void) last_colon;
			(void) first_colon;
			(void) end;
		}
		else
		{
			emit(severity, NULL, 0, p);
		}

		g_free(work);
		return;
	}

	/* Passthrough for non-pdc noise (still useful in Compiler tab). */
	msgwin_compiler_add_string(COLOR_BLACK, work);
	msg_count++;
	g_free(work);
}


void pd_errors_end(gint exit_status)
{
	if (exit_status == 0)
	{
		msgwin_compiler_add(COLOR_BLUE, _("Playdate: build succeeded (%u message%s)"),
			msg_count, msg_count == 1 ? "" : "s");
	}
	else
	{
		msgwin_compiler_add(COLOR_RED,
			_("Playdate: build failed (exit %d) — %u error(s), %u warning(s)"),
			exit_status, error_count, warn_count);
	}
}
