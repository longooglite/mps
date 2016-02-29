package edu.umich.umms.open.controller.json;

import edu.umich.umms.ldap.Person;
import edu.umich.umms.ldap.PersonLookupService;
import edu.umich.umms.open.response.UniqnameResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ldap.NameNotFoundException;
import org.springframework.ldap.ServiceUnavailableException;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.ModelMap;
import org.springframework.core.env.Environment;

import javax.annotation.Resource;


@Controller
@RequestMapping("/public/uniqname")
public class UniqnameController {
    @Resource PersonLookupService personLookupService;
    
    @Resource
    private Environment env;

    @ResponseBody
    @RequestMapping(value = "/find/{uniqname}", method = RequestMethod.GET)
    public UniqnameResponse findUniqname(@PathVariable String uniqname, ModelMap model) {
        if (env.getProperty("env").equals("dev"))
        {
            String first = uniqname.substring(0,1).toUpperCase();
            String last = uniqname.substring(1).toUpperCase();
            return new UniqnameResponse(first, last, "", "", uniqname);
        }
        try {
            Person person = personLookupService.lookupByUniqname(uniqname);
            model.addAttribute("person", person);
            model.addAttribute("uniqname", uniqname);
            return new UniqnameResponse(person);
        } catch (NameNotFoundException nnfe) {
            model.addAttribute("nnfe", nnfe);
            throw nnfe;
        } catch (Throwable t) {
            throw new ServiceUnavailableException(
                    new javax.naming.ServiceUnavailableException("Error in lookup. Try again."));
        }
    }



    @ExceptionHandler({NameNotFoundException.class})
    public ResponseEntity<String> handleNameNotFoundException(NameNotFoundException exception) {
        return new ResponseEntity<String>("uniqname not found", HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler({ServiceUnavailableException.class})
    public ResponseEntity<String> handleServiceUnavailableException(ServiceUnavailableException exception) {
        return new ResponseEntity<String>(
                "Uniqname lookup functionality temporarily unavailable. Try again in a few minutes.",
                HttpStatus.NOT_FOUND);
    }
}
