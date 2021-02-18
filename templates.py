import jinja2
from jinja2 import Environment, PackageLoader

package_loader = PackageLoader("templates")
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=package_loader)



def template(template_name: str) -> jinja2.Template:
    """Get the template object given the name.

    Args:
      template_name: The name of the template file (.html)

    Returns:
      The jinja2 environment.

    """
    return jinja2_env.get_template(template_name)

